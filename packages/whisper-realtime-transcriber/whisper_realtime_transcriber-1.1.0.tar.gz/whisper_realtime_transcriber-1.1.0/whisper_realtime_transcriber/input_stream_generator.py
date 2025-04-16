import numpy as np
import asyncio
import sys
from copy import deepcopy

from pydantic import BaseModel, Field
from typing import AsyncGenerator
import soundfile as sf
import resampy
import platform

try:
    import sounddevice as sd
except OSError as e:
    print(e)
    print("If `GLIBCXX_x.x.x' not found, try installing it with: conda install -c conda-forge libstdcxx-ng=12")
    sys.exit()


class GeneratorConfig(BaseModel):
    samplerate: int = Field(
        default=16000,
        description={"help": "The specified samplerate of the audio data."},
    )
    blocksize: int = Field(
        default=2000,
        description={"help": "The size of each individual audio chunk."},
    )
    adjustment_time: int = Field(
        default=5,
        description={"help": "The adjustment_time for setting the silence threshold."},
    )
    min_chunks: int = Field(
        default=6,
        description={"help": "The minimum number of chunks to be generated, before feeding it into the asr model."},
    )
    phrase_delta: float = Field(
        default=1.25,
        description={"help": "The expected pause between two phrases in seconds."},
    )
    continuous: bool = Field(
        default=True,
        description={"help": "Whether to generate audio data conituously or not."},
    )
    from_file: str = Field(
        default=None,
        description={"help": "The path to the audio file to be used for inference."},
    )
    from_output_device: bool = Field(
        default=None,
        description={"help": "If the output device should be used for inference."},
    )
    verbose: bool = Field(
        default=True,
        description={"help": "Whether to print the additional information to the console or not."},
    )


class InputStreamGenerator:
    """
    Loading and using the InputStreamGenerator.

    Methods
    -------
    process_audio()
        Processes the incoming audio data.
    """

    def __init__(self, generator_config: GeneratorConfig):
        self.samplerate = generator_config.samplerate
        self._blocksize = generator_config.blocksize
        self._adjustment_time = generator_config.adjustment_time
        self._min_chunks = generator_config.min_chunks
        self._continuous = generator_config.continuous
        self._verbose = generator_config.verbose
        
        self.from_file = generator_config.from_file
        self.use_loopback = generator_config.from_output_device

        self._global_ndarray: np.ndarray = None
        self.temp_ndarray: np.ndarray = None

        self._phrase_delta_blocks: int = int((self.samplerate // self._blocksize) * generator_config.phrase_delta)
        self.complete_phrase_event = asyncio.Event()

        self._silence_threshold: float = -1

        self.data_ready_event = asyncio.Event()

    async def generate_from_file(self, file_path: str) -> AsyncGenerator:
        """
        Generate audio chunks from a file instead of a live microphone.
        """
        data, samplerate = sf.read(file_path, dtype='float32')
        
        if samplerate != self.samplerate:
            data = resampy.resample(data.astype(np.float32), samplerate, self.samplerate)
            data = (data * 32767).astype(np.int16)  # convert back to int16 after resampling

        # Reshape if mono audio is expected
        if data.ndim > 1:
            data = data[:, 0]

        total_samples = len(data)
        idx = 0
        while idx < total_samples:
            chunk = data[idx:idx + self._blocksize]
            idx += self._blocksize
            await asyncio.sleep(self._blocksize / self.samplerate)  # simulate real-time delay
            yield chunk, None  # Second value simulates the 'status'
    
    async def _generate(self) -> AsyncGenerator:
        """
        Generate audio chunks of size of the blocksize and yield them.
        """
        if self.from_file:
            async for chunk, status in self.generate_from_file(self.from_file):
                yield chunk, status
            return
        
        q_in = asyncio.Queue()
        loop = asyncio.get_event_loop()

        def callback(in_data, _, __, state):
            loop.call_soon_threadsafe(q_in.put_nowait, (in_data.copy(), state))
            
        # Default stream args
        stream_args = dict(
            samplerate=self.samplerate,
            channels=1,
            dtype="int16",
            blocksize=self._blocksize,
            callback=callback,
        )
            
        if self.use_loopback:
            if platform.system() != "Linux":
                raise RuntimeError("Loopback streaming is only supported on Linux in this implementation.")
            # Find a PulseAudio monitor device
            devices = sd.query_devices()
            monitor_name = self.output_device or next(
                (d['name'] for d in devices if 'Monitor' in d['name']), None
            )
            if not monitor_name:
                raise RuntimeError("No monitor (loopback) device found. Is PulseAudio running?")
            stream_args["device"] = monitor_name

        stream = sd.InputStream(
            **stream_args,
        )
        with stream:
            while True:
                indata, status = await q_in.get()
                yield indata, status

    async def process_audio(self) -> None:
        """
        Continuously processes audio input, detects significant speech segments, and prepares them for transcription.

        This method handles real-time audio data processing, identifying meaningful speech segments while discarding
        silence and noise. It aggregates valid audio chunks for transcription and manages the flow based on a
        silence threshold, memory-safe mode, and whether the system is in continuous mode or not.

        Workflow:
            1. **Set Silence Threshold**:
               - If the silence threshold (`_silence_threshold`) is not initialized, the method calls `_set_silence_threshold()`
                 to set the value dynamically based on ambient sound.

            2. **Listening Loop**:
               - The method enters an asynchronous loop, consuming audio buffers generated by `_generate()`.
               - It processes each audio buffer (`indata`), which represents the current audio input stream.

            3. **Silence Detection**:
               - For each buffer, the method flattens and analyzes the absolute values of the audio data.
               - Buffers that mostly contain silence (i.e., below the silence threshold) are discarded unless they are part
                 of an ongoing phrase stored in `self._global_ndarray`.
               - In memory-safe mode, buffers are discarded if `data_ready_event` is set, to ensure efficient memory usage.

            4. **Buffer Concatenation**:
               - If there is already ongoing audio data stored in `self._global_ndarray`, the new buffer is concatenated to it.
               - If not, the current buffer initializes `self._global_ndarray` and starts the phrase collection.

            5. **End-of-Buffer Check**:
               - At the end of each buffer, the method determines if the buffer contains significant speech.
               - If it does not detect speech and the collected data exceeds the required minimum chunk size (`_min_chunks`),
                 the following actions are performed:
                   - The accumulated data is copied to `self.temp_ndarray`, flattened, and normalized.
                   - `self._global_ndarray` is reset to `None` to begin a new phrase.
                   - The `data_ready_event` is set to notify that the audio chunk is ready for transcription.

            6. **Phrase Completion**:
               - If silence is detected beyond a certain threshold (`_phrase_delta_blocks`), the phrase is considered complete.
               - The method sets `complete_phrase_event` and sends the audio for transcription by calling `_send_audio()`.

            7. **Continuous Mode Check**:
               - If the `continuous` mode is disabled, the method exits after processing the first valid chunk of audio.
               - If `continuous` mode is enabled, it continues looping to process incoming audio indefinitely.

        Returns:
            None: This method runs indefinitely in continuous mode, continuously processing and preparing audio data
            for transcription. If `continuous` mode is disabled, it returns after processing the first valid audio chunk.
        """

        if self._silence_threshold < 0 and (self.from_file or self.use_loopback is None):
            self._silence_threshold = 25
            # await self._set_silence_threshold()
        else:
            self._silence_threshold = 25

        print("Listening...")
        empty_blocks = 0

        async for indata, _ in self._generate():
            indata_flattened: np.ndarray = abs(indata.flatten())
            if self._global_ndarray is not None and np.percentile(indata_flattened, 10) <= self._silence_threshold:
                empty_blocks += 1
                if empty_blocks >= self._phrase_delta_blocks:
                    empty_blocks = 0
                    self.complete_phrase_event.set()
                    await self._send_audio() if not self.data_ready_event.is_set() else None
                    if not self._continuous:
                        return None
                continue

            # discard buffers that contain mostly silence
            if (
                np.percentile(indata_flattened, 10) <= self._silence_threshold and self._global_ndarray is None
            ) or self.data_ready_event.is_set():
                continue

            # concatenate buffers
            if self._global_ndarray is not None:
                self._global_ndarray = np.concatenate((self._global_ndarray, indata), dtype="int16")
            else:
                self._global_ndarray = indata

            empty_blocks = 0

            if (np.percentile(indata_flattened[-100:-1], 10) > self._silence_threshold) or self.data_ready_event.is_set():
                continue

            # Process the global ndarray if the required chunks are met
            if len(self._global_ndarray) / self._blocksize >= self._min_chunks:
                await self._send_audio()

    async def _send_audio(self):
        self.temp_ndarray = deepcopy(self._global_ndarray)
        self._global_ndarray = None
        self.data_ready_event.set()

    async def _set_silence_threshold(self) -> None:
        """
        Dynamically sets the silence threshold for audio processing based on the average loudness of initial audio blocks.

        This method listens to the initial few seconds of audio input to determine an appropriate silence threshold.
        It calculates the loudness of the audio blocks during this period and sets the silence threshold to the 20th percentile
        of the observed loudness values. This threshold is used later to differentiate between significant audio and silence.

        Workflow:
            1. **Initialize Variables**:
                - `blocks_processed`: Tracks the number of audio blocks processed.
                - `loudness_values`: Stores the mean loudness of each audio block for later analysis.

            2. **Audio Block Processing**:
                - The method enters an asynchronous loop where it continuously processes audio blocks generated by `_generate()`.
                - For each block, it calculates the mean loudness and adds it to `loudness_values`.

            3. **Threshold Adjustment**:
                - The method continues processing until it has processed a sufficient number of blocks (determined by `_adjustment_time`).
                - Once enough blocks have been processed, it calculates the silence threshold as the 20th percentile of the collected
                  loudness values.
                - This ensures that the threshold is set to a level that filters out most of the silence while capturing meaningful audio.

            4. **Verbose Output**:
                - If `verbose` mode is enabled, the method prints the newly set silence threshold for debugging or informational purposes.

        Returns:
            None: The method sets the silence threshold and then exits. It does not return any value.
        """

        blocks_processed: int = 0
        loudness_values: list = []

        async for indata, _ in self._generate():
            blocks_processed += 1
            indata_flattened: np.ndarray = abs(indata.flatten())

            # Compute loudness over first few seconds to adjust silence threshold
            loudness_values.append(np.mean(indata_flattened))

            # Stop recording after ADJUSTMENT_TIME seconds
            if blocks_processed >= self._adjustment_time * (self.samplerate / self._blocksize):
                self._silence_threshold = float(np.percentile(loudness_values, 10))
                break

        if self._verbose:
            print(f"Set SILENCE_THRESHOLD to {self._silence_threshold}\n")

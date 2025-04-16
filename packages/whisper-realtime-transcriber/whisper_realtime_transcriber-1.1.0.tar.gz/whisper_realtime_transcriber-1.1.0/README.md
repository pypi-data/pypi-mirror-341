# Whisper Realtime Transcriber

## Overview

This [repository](https://github.com/nico-byte/whisper-realtime-transcriber) contains the source code of a realtime transcriber for various [whisper](https://github.com/openai/whisper) models, published on [huggingface](https://github.com/huggingface/transformers).

## Prerequisites

- [Python 3.10.12](https://www.python.org) installed on the machine.
- Microphone connected to the machine.

## Installation

1. **Install project from source**
    ```bash
    git clone 

    sh ./install.sh
    ```
2. **Install the package via pip:**
      ```bash
      pip install --upgrade whisper-realtime-transcriber
      ```

## Usage

After completing the installation, one can now use the transcriber:

  - Necessary imports
  ```python
  import asyncio

  from whisper_realtime_transcriber.realtime_transcriber import RealtimeTranscriber
  ```

  - Standard way - model and generator are initialized by the RealtimeTranscriber and all outputs get printed directly to the console.
  ```python
  transcriber = RealtimeTranscriber()

  asyncio.run(transcriber.execute_event_loop())
  ```

  - Launching the TranscriptionAPI
  ```python

  from whisper_realtime_transcriber.api import TranscriptionAPI
  
  # The API will send the transcriptions to http://localhost:8000 if not further specified
  api = TranscriptionAPI(transcriber.asr_model)
    
  api.run()

  asyncio.run(transcriber.execute_event_loop())
  # Now one can access the transcriptions via http://localhost:8000
  ```

  - Loading the InputStreamGenerator and/or Whisper Model with custom values.
  ```python
  from whisper_realtime_transcriber.inputstream_generator import GeneratorConfig
  from whisper_realtime_transcriber.whisper_model import ModelConfig
  
  generator_config = GeneratorConfig(samplerate=8000, blocksize=2000, min_chunks=2)
  model_config = ModelConfig(inputstream_generator, model_id="openai/whisper-tiny", device="cuda")

  transcriber = RealtimeTranscriber(generator_config, model_config)

  asyncio.run(transcriber.execute_event_loop())
  ```

Feel free to reach out if you encounter any issues or have questions!

## How it works

- The transcriber consists of two modules: a Inputstream Generator and a Whisper Model.
- The implementation of the Inputstream Generator is based on this [implemantation](https://github.com/tobiashuttinger/openai-whisper-realtime).
- The Inputstream Generator reads the microphone input and passes it to the Whisper Model. The Whisper Model then generates the transcription.
- This is happening in an async event loop so that the Whsiper Model can continuously generate transcriptions from the provided audio input, generated and processed by the Inputstream Generator.
- On a machine with a 12GB Nvidia RTX 3060 the [distilled large-v3](https://github.com/huggingface/distil-whisper) model runs at a realtime-factor of about 0.4, this means 10s of audio input get transcribed in 4s - the longer the input the bigger is the realtime-factor.

## ToDos

- Add functionality to transcribe from audio files.
- Get somehow rid of the hallucinations of the whisper models when no voice is active.
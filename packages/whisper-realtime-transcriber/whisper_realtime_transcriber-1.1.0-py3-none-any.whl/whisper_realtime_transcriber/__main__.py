import asyncio
import sys

from whisper_realtime_transcriber.input_stream_generator import GeneratorConfig
from whisper_realtime_transcriber.whisper_model import ModelConfig
from whisper_realtime_transcriber.realtime_transcriber import RealtimeTranscriber
from whisper_realtime_transcriber.api import TranscriptionAPI, print_transcriptions_loop


async def main():
    model_config = ModelConfig(device="cuda")
    generator_config = GeneratorConfig()

    transcriber = RealtimeTranscriber(model_config=model_config, generator_config=generator_config)

    # Start API
    api = TranscriptionAPI(transcriber.asr_model)
    api.run()

    # Start all tasks in parallel
    await asyncio.gather(
        transcriber.execute_event_loop(),
        print_transcriptions_loop(transcriber.asr_model),
    )


if __name__ == "__main__":
    try:
        print("Activating wire...")
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit("\nInterrupted by user")
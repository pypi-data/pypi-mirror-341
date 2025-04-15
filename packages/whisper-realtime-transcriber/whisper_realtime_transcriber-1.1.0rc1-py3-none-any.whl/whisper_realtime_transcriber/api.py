from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import threading
import asyncio
import os
import sys

from typing import List

from whisper_realtime_transcriber.whisper_model import WhisperModel


class TranscriptionAPI:
    def __init__(self, transcriber: WhisperModel, host: str = "localhost", port: int = 8000):
        self.transcriber = transcriber
        self.app = FastAPI()
        self.host = host
        self.port = port

        @self.app.get("/transcriptions")
        async def get_transcriptions():
            return JSONResponse(content={"transcriptions": self.transcriber.get_transcriptions()})

    def run(self):
        # Run API in a background thread
        threading.Thread(
            target=uvicorn.run,
            kwargs={"app": self.app, "host": self.host, "port": self.port},
            daemon=True,
        ).start()


# Keep track of previous line count across calls
_last_line_count = 0

async def _print_transcriptions(transcriptions: List[str]) -> None:
    """
    Prints the model transcription, overwriting previous output.
    """
    global _last_line_count

    output = [t for t in transcriptions if t.strip() != ""]

    # Move cursor up to overwrite previous output
    if _last_line_count > 0:
        sys.stdout.write(f"\033[{_last_line_count}A")  # Move cursor up
        sys.stdout.flush()

    formatted_lines = []
    for transcription in output:
        words = transcription.split(" ")
        line_count = 0
        split_input = ""
        for word in words:
            line_count += 1 + len(word)
            if line_count > os.get_terminal_size().columns:
                split_input += "\n"
                line_count = len(word) + 1
            split_input += word + " "
        formatted_lines.extend(split_input.rstrip().split("\n"))

    # Clear and print each new line
    for line in formatted_lines:
        sys.stdout.write("\033[K")  # Clear line
        print(line)

    sys.stdout.flush()
    _last_line_count = len(formatted_lines)


async def print_transcriptions_loop(transcriber: WhisperModel, interval: float = 1.0):
    """
    Continuously prints transcriptions from the transcriber every `interval` seconds.
    """
    while True:
        await _print_transcriptions(transcriptions=transcriber.get_transcriptions())
        await asyncio.sleep(interval)

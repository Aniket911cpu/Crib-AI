import asyncio
import soundcard as sc
import numpy as np
import threading
import json
import os
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
)

# Configuration
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
SAMPLE_RATE = 16000
CHANNELS = 1  # Mono for ASR

class AudioStreamer:
    def __init__(self):
        self.loopback_mic = sc.default_speaker() # WASAPI loopback captures "speakers"
        self.is_running = False
        self.dg_connection = None

    def _get_loopback_mic(self):
        """Finds the default speaker for loopback capture."""
        try:
            return sc.default_speaker()
        except Exception as e:
            print(f"Error finding loopback device: {e}")
            return None

    def _audio_callback(self, indata, frames, time, status):
        """Callback for capturing audio chunks."""
        if self.dg_connection:
            # Convert float32 numpy array to valid bytes for Deepgram (int16)
            # soundcard returns float32 [-1.0, 1.0]
            audio_data = (indata * 32767).astype(np.int16).tobytes()
            self.dg_connection.send(audio_data)

    async def start_transcription(self):
        print("Initializing Deepgram Client...")
        if not DEEPGRAM_API_KEY:
            print("Error: DEEPGRAM_API_KEY not found in environment.")
            return

        try:
            # Initialize Deepgram
            config = DeepgramClientOptions(options={"keepalive": "true"})
            deepgram = DeepgramClient(DEEPGRAM_API_KEY, config)

            # Create WebSocket connection
            self.dg_connection = deepgram.listen.asyncwebsocket.v("1")

            # Event Handlers
            def on_message(self, result, **kwargs):
                sentence = result.channel.alternatives[0].transcript
                if len(sentence) > 0:
                    print(f"Transcript: {sentence}")
                    # TODO: Send this transcript to the Frontend via WebSocket/IPC

            def on_error(self, error, **kwargs):
                print(f"Deepgram Error: {error}")

            self.dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            self.dg_connection.on(LiveTranscriptionEvents.Error, on_error)

            # Start Connection
            options = LiveOptions(
                model="nova-2",
                language="en-US",
                smart_format=True,
                encoding="linear16",
                channels=CHANNELS,
                sample_rate=SAMPLE_RATE,
                interim_results=True,
                utc=True,
                endpointing=300, # 300ms silence = end of utterance
            )

            if await self.dg_connection.start(options) is False:
                print("Failed to start Deepgram connection")
                return

            print("Deepgram Connected. Starting Audio Loopback...")
            
            # Start Recording Loop
            self.is_running = True
            with self.loopback_mic.recorder(samplerate=SAMPLE_RATE, channels=CHANNELS) as mic:
                while self.is_running:
                    # Record 100ms chunks
                    data = mic.record(numframes=int(SAMPLE_RATE * 0.1))
                    # Convert to int16 bytes
                    audio_bytes = (data[:, 0] * 32767).astype(np.int16).tobytes()
                    # Send to Deepgram
                    await self.dg_connection.send(audio_bytes)
                    await asyncio.sleep(0.01)

        except Exception as e:
            print(f"Exception: {e}")
        finally:
            if self.dg_connection:
                await self.dg_connection.finish()

    def stop(self):
        self.is_running = False

if __name__ == "__main__":
    # Test runner
    streamer = AudioStreamer()
    asyncio.run(streamer.start_transcription())

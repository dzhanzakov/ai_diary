#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from openai import OpenAI
from pydub import AudioSegment
from pydub.utils import make_chunks
from pathlib import Path
from dotenv import load_dotenv
from crew import TranscriberCrew
import os

load_dotenv()

print("🔑 OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

client = OpenAI()

class TranscriberState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""


class TranscriberFlow(Flow[TranscriberState]):

    @start()
    def transcribe_meeting(self):
        print("Generating Transcription")

        SCRIPT_DIR = Path(__file__).parent
        audio_path = str(SCRIPT_DIR / "output.wav")
        
        audio = AudioSegment.from_file(audio_path, format="wav")
        
        chunk_length_ms = 60000
        chunks = make_chunks(audio, chunk_length_ms)

        full_transcription = ""
        for i, chunk in enumerate(chunks):
            print(f"Transcribing chunk {i+1}/{len(chunks)}")
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            
            with open(chunk_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                full_transcription += transcription.text + " "

        self.state.transcript = full_transcription
        print(f"Transcription: {self.state.transcript}")

    @listen(transcribe_meeting)
    def generate_meeting_minutes(self):
        print("Generating Meeting Minutes")

        crew = TranscriberCrew()

        inputs = {
            "transcript": self.state.transcript
        }
        meeting_minutes = crew.crew().kickoff(inputs)
        self.state.meeting_minutes = str(meeting_minutes)

    

def kickoff():


    meeting_minutes_flow = TranscriberFlow()
    meeting_minutes_flow.plot()
    meeting_minutes_flow.kickoff()



if __name__ == "__main__":
    kickoff()
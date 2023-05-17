import os

from fastapi import UploadFile
from pydub import AudioSegment


def convert_wav_to_mpa3(file: UploadFile, record_id):
    audio = AudioSegment.from_file(file.file, format="wav")
    record_path = os.path.join("records", f"{record_id}.mp3")
    print(record_path)
    audio.export(record_path, format="mp3")


def generate_record_url(record_id: str, user_id: str, host: str) -> str:
    return f"http://{host}/api_v1/record?record_id={record_id}&user_id={user_id}"

import os
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File
from pydub import AudioSegment
from starlette.responses import FileResponse

router = APIRouter()

@router.post("/records/")
async def add_record(user_id: str, access_token: str, file: UploadFile = File(...)):

    if user_id in users_db and users_db[user_id]["access_token"] == access_token:

        audio = AudioSegment.from_file(file.file, format="wav")
        record_id = str(uuid4())
        record_url = f"http://host:port/record?id={record_id}&user={user_id}"
        record_path = os.path.join("records", f"{record_id}.mp3")
        audio.export(record_path, format="mp3")
        return {"record_url": record_url}
    else:
        return {"error": "User not found or wrong token"}


@router.get("/record/")
async def get_record(record_id: str, user_id: str):
    if user_id in users_db and f"records/{record_id}.mp3" in os.listdir():
        return FileResponse(f"{record_id}.mp3")
    else:
        return {"error": "Запись не найдена или доступ запрещен"}
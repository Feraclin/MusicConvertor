from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Request, HTTPException, Depends
from starlette.responses import FileResponse
from api.app.api_v1.deps import app_dependency, user_dependency, get_user_by_id
from api.app.models import UserModel
from api.app.utils import convert_wav_to_mpa3, generate_record_url

router = APIRouter()


@router.post("/record/")
async def add_record(
    user: U
    request: Request,
    file: UploadFile = File(...),
    app=app_dependency,
    user: UserModel = user_dependency,
):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        record_id = str(uuid4())
        print("test")
        convert_wav_to_mpa3(file=file, record_id=record_id)
        await app.state.records.add_record_to_db(
            user_id=user.id_, record_id=record_id, title=file.filename.rstrip(".wav")
        )
        record_url = generate_record_url(
            user_id=user.id_, record_id=record_id, host=request.headers.get("host")
        )
        return {"record_url": record_url}
    except Exception as e:
        app.state.logger.info(e)
        raise HTTPException(status_code=418)


@router.get("/record")
async def get_record(
    record_id: str,
    app=app_dependency,
    user: UserModel = Depends(get_user_by_id)
):
    base_dir = Path(__file__).resolve().parent.parent.parent / "records"
    record = base_dir / f"{record_id}.mp3"
    title = await app.state.records.get_record_title(record_id=record_id)
    if user:
        if record.exists():
            return FileResponse(record, filename=title)
        else:
            raise HTTPException(status_code=404, detail="Record not found")
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/record/list")
async def get_record_list_by_user(
    access_token: str,
    request: Request,
    app=app_dependency,
    user=Depends(get_user_by_id)
):

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if str(user.access_token) != access_token:
        raise HTTPException(status_code=403, detail="Access token established or wrong")

    record_list = (
        await app.state.records.get_records_list_by_user(user_id=user.id_)
    ).all()
    record_dct = {
        k.title: generate_record_url(
            user_id=user.id_, record_id=k.record_id, host=request.headers.get("host")
        )
        for k in record_list
    }
    return record_dct


@router.get("/teapot")
async def teapot():
    raise HTTPException(status_code=418)

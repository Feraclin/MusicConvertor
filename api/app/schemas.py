from pydantic import BaseModel

from api.app.models import RecordModel, UserModel

RecordSchema = RecordModel.__pydantic_model__.schema()


class UserNameRequest(BaseModel):
    username: str


class UserIdRequest(BaseModel):
    user_id: str


class RecordRequest(BaseModel):
    record_id: str


class RecordListResponse(BaseModel):
    records: list[RecordModel]


class UserRequest(BaseModel):
    user_id: str
    access_token: str

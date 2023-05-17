from pydantic import BaseModel

from api.app.models import RecordModel

RecordSchema = RecordModel.__pydantic_model__.schema()


class RecordListResponse(BaseModel):
    records: list[RecordModel]


print(RecordSchema)

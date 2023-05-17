from fastapi import APIRouter

router = APIRouter()

@router.post("/users/")
async def create_user(username: str):

    user_id = str(uuid4())
    access_token = str(uuid4())
    users_db[user_id] = {"username": username, "access_token": access_token}
    return {"user_id": user_id, "access_token": access_token}

from fastapi import Depends, Request


async def get_app(request: Request):
    return request.app


async def get_user_by_id(user_id: str, request: Request):
    user = await request.app.state.users.get_user_by_id(user_id)
    return user


app_dependency = Depends(get_app)
user_dependency = Depends(get_user_by_id)

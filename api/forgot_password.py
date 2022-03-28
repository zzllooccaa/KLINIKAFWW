from fastapi import APIRouter, HTTPException, Header
from starlette.responses import JSONResponse

from uuid import uuid4
from model import User, db
from api.gmail import send_mail

import errors
import schemas

forgot_password_router = APIRouter()


@forgot_password_router.patch("/forgot-password")
async def forgot_password(item: schemas.ForgotPassword):
    user_one = User.get_user_by_email(email=item.email)
    if not user_one:
        raise HTTPException(status_code=400, detail=errors.WRONG_CREDENTIALS)

    user_one.hashed_password = uuid4()
    db.add(user_one)
    db.commit()

    await send_mail(email=user_one.email, token=user_one.hashed_password)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@forgot_password_router.patch("/recover-password")
async def forgot_password(item: schemas.RecoverPassword, session_id: str = Header(None)):
    if session_id:
        user = User.get_user_recover(hashed_password=session_id)
        if not user:
            return HTTPException(status_code=400, detail=errors.WRONG_CREDENTIALS)
        user.password = item.password
        db.add(user)
        db.commit()
        return user
    raise HTTPException(status_code=400, detail=errors.WRONG_CREDENTIALS)

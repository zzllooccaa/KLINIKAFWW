import fastapi_mail.msg

from model import User, db
from fastapi import APIRouter, HTTPException, Header
from uuid import uuid4
import errors
import schemas

forgot_password_router = APIRouter()


@forgot_password_router.patch("/forgot-password")
async def forgot_password(item: schemas.ForgotPassword):
    user_one = User.get_user_by_email(email=item.email)
    print(user_one)
    if not user_one:
        raise HTTPException(status_code=400, detail=errors.WRONG_CREDENTIALS)
    user_one.hashed_password = uuid4()
    print(user_one.hashed_password)
    db.add(user_one)
    db.commit()
    data = item.email
    a1 = open('user_mail.txt', 'w')
    a1.write(data)
    a1.close()
    print(data)
    return user_one


@forgot_password_router.patch("/recover-password")
async def forgot_password(item: schemas.RecoverPassword, session_id: str = Header(None)):
    if session_id:
        user = User.get_user_recover(hashed_password=session_id)
        user.password = item.password
        db.add(user)
        db.commit()
        return user
    raise HTTPException(status_code=400, detail=errors.WRONG_CREDENTIALS)

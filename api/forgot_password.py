from model import User, db
from fastapi import APIRouter, HTTPException, Header
from uuid import uuid4
import errors
import schemas
from api.gmail import send_mail

forgot_password_router = APIRouter()


@forgot_password_router.patch("/forgot-password")
async def forgot_password(item: schemas.ForgotPassword):
    user_one = User.get_user_by_email(email=item.email)
    if not user_one:
        raise HTTPException(status_code=400, detail=errors.WRONG_CREDENTIALS)
    user_one.hashed_password = uuid4()
    db.add(user_one)
    db.commit()
    db.refresh(user_one)
    data = item.email
    a1 = open('/home/fww1/PycharmProjects/pythonProject/clinic45/temp/user_mail.txt', 'w')
    a1.write(data)
    a1.close()
    data_hash = user_one.hashed_password
    a2 = open('/home/fww1/PycharmProjects/pythonProject/clinic45/temp/hashed_password.txt', 'w')
    a2.write(data_hash)
    a2.close()
    await send_mail()
    return user_one


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

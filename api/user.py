from fastapi import APIRouter, Response, Depends
from model import User, db, Role
import schemas
from uuid import uuid4

from sess.sess_verifier import backend_exm
from sess.sess_fronted import cookie
from sess.sess_verifier import SessionData, verifier

import errors

user_router = APIRouter()


@user_router.post("/login")
async def login(item: schemas.UserLogin, response: Response):
    user = User.get_user_by_email_and_password(email=item.email, password=item.password)
    if not user:
        return {"ERROR": errors.WRONG_CREDENTIALS}

    session = uuid4()
    data = schemas.SessionData(
        username=user.name,
        role=user.role,
        id=user.id,
    )
    await backend_exm.create(session, data)
    cookie.attach_to_response(response, session)
    return user


@user_router.post("/create", dependencies=[Depends(cookie)])
def create_user(item: schemas.UserRegisterLogin, session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.admin.name:
        return errors.ERR_USER_NOT_GRANTED
    if User.check_user_by_email(email=item.email):  # Todo upotrebi or funkciju pogledaj u sqlalchemyiju
        return errors.ERR_USER_ALREADY_EXIST

    if User.check_user_by_jmbg(jmbg=item.jmbg):
        return errors.ERR_USER_JMBG_ALREADY_EXIST
    try:
        user = User(
            email=item.email,
            password=item.password,
            name=item.name,
            surname=item.surname,
            jmbg=item.jmbg,
            role=item.role
        )
        db.add(user)
        db.commit()
        return user

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@user_router.patch("/{user_id}", dependencies=[Depends(cookie)], status_code=200)
def edit(user_id, user_data: schemas.BaseUserSchema, session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.admin.name:
        return errors.ERR_USER_NOT_GRANTED
    user = User.get_by_id(id=user_id)
    if not user:
        return {"ERROR": "User id not exist"}

    user_data_dict = user_data.dict(exclude_none=True)
    try:
        User.edit_user(user_id=user_id, user_data=user_data_dict)
        db.add(user)
        db.commit()

    except Exception as e:
        if 'duplicate key value violates unique constraint' in str(e):
            return {"ERROR": "ERR_DUPLICATED_ENTRY"}

        return {"ERROR": "ERR_CANNOT_EDIT_USER"}

    return user


@user_router.get("/all_users", dependencies=[Depends(cookie)], status_code=200)
def get_all_user(email: str = None, name: str = None, surname: str = None,
                 session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.admin.name:
        return errors.ERR_USER_NOT_GRANTED

    users = User.get_all_user_paginate(email=email, name=name, surname=surname)
    return users












#TOdo Pogledaj paginate sqlalchemy i vidi kako da vratis 10 korisnika iz prve strane
# Add filter LIKE in sqlaalchemy
# jedan poziv koji ce  mi vratiti sve korisnike ili recimo prvih 10

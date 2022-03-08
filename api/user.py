from fastapi import APIRouter, Response, Depends, Body
from model import User, db
import schemas
from uuid import UUID, uuid4
from utils import auth_user
from examples import user_example

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


@user_router.get('/logout')
def del_session(response: Response, session_id: UUID = Depends(cookie)):
    backend_exm.delete(session_id)
    cookie.delete_from_response(response)
    return "You have logged out successfully"


@user_router.post("/create_user", dependencies=[Depends(cookie)])
def create_user(item: schemas.RegisterUser = user_example, session_data: SessionData = Depends(verifier)):
    auth_user(user=session_data, roles=['admin'])
    if User.check_user_by_email(email=item.email):
        return errors.ERR_USER_ALREADY_EXIST

    try:
        user = User(
            email=item.email,
            password=item.password,
            name=item.name,
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
def edit(user_id: int, user_data: schemas.UserUpdate, session_data: SessionData = Depends(verifier)):
    auth_user(user=session_data, roles=['admin'])
    user = User.get_user_by_id(id=user_id)
    if not user:
        return errors.ERR_ID_NOT_EXIST

    user_d = user_data.dict(exclude_unset=True)
    print(user_d)
    for key, value in user_d.items():
        setattr(user[0], key, value)
    db.add(user[0])
    db.commit()
    db.refresh(user[0])
    return user


@user_router.get("/all_users", dependencies=[Depends(cookie)], status_code=200)
def get_all_user(email: str = None, name: str = None,
                 session_data: SessionData = Depends(verifier)):
    auth_user(user=session_data, roles=['admin'])
    users = User.get_all_user_paginate(email=email, name=name)
    print(users[0].role)
    return users


@user_router.get("/users_by_role", dependencies=[Depends(cookie)], status_code=200)
def get_user_by_role(user_by_role, session_data: SessionData = Depends(verifier)):
    search_user = User.check_user_by_role(role=user_by_role)
    auth_user(user=session_data, roles=['admin'])
    if not search_user:
        return errors.ERR_CHECK_YOUR_TYPE
    return search_user


@user_router.delete("/{delete_by_id}", dependencies=[Depends(cookie)], status_code=200)
def delete_user(delete_user, session_data: SessionData = Depends(verifier)):
    auth_user(user=session_data, roles=['admin'])
    user = User.get_by_id(id=delete_user)
    if not user:
        return errors.ERR_ID_NOT_EXIST
    db.delete(user)
    db.commit()
    return {}

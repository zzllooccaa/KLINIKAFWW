from fastapi import APIRouter, Depends, HTTPException
from model import User, db
import schemas
from uuid import uuid4

from examples import user_example
from fastapi.encoders import jsonable_encoder
from utils import auth_user, get_user_from_header

from sess.sess_fronted import cookie

import errors

user_router = APIRouter()


def _update_user_session(user, session_id):
    """Update user session_id"""
    user.session_id = session_id
    db.add(user)
    db.commit()
    return user


@user_router.post("/login")
async def login(item: schemas.UserLogin):
    user = User.get_user_by_email_and_password(email=item.email, password=item.password)
    if not user:
        raise HTTPException(status_code=400, detail=errors.WRONG_CREDENTIALS)

    return _update_user_session(user=user, session_id='{}:{}'.format(user.id, uuid4()))


@user_router.get('/logout')
def del_session(current_user: User = Depends(get_user_from_header)):
    _update_user_session(user=current_user, session_id=None)
    return {}


@user_router.post("/create_user")
def create_user(item: schemas.RegisterUser = user_example, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    if User.check_user_by_email(email=item.email):
        return HTTPException(status_code=400, detail=errors.ERR_USER_ALREADY_EXIST)

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


@user_router.get("/user/{user_id}", dependencies=[Depends(cookie)], status_code=200)
def get_user_by_id(user_id, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    # return user[user_id]
    return User.get_by_id(id=user_id)


@user_router.patch("/user/{user_id}", dependencies=[Depends(cookie)], status_code=200)
def edit(user_id: int, user_data: schemas.UserUpdate, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    user = User.get_user_by_id(id=user_id)
    if not user:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    stored_item_data = User[user_id]
    stored_item_model = User(**stored_item_data)
    update_data = user_data.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    user[user_id] = jsonable_encoder(updated_item)
    return updated_item
    # user_d = schemas.UserUpdate
    # user_d = user_data.dict(exclude_unset=True)
    # print(user_d)
    # for key, value in user_d.items():
    #     setattr(user[0], key, value)
    # db.add(user_d)
    # db.commit()
    # db.refresh(user_d)
    # return user


@user_router.get("/all_users", dependencies=[Depends(cookie)], status_code=200)
def get_all_user(email: str = None, name: str = None,
                 current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    users = User.get_all_user_paginate(email=email, name=name)
    print(users[0].role)
    return users


@user_router.get("/users_by_role", dependencies=[Depends(cookie)], status_code=200)
def get_user_by_role(user_by_role, current_user: User = Depends(get_user_from_header)):
    search_user = User.check_user_by_role(role=user_by_role)
    auth_user(user=current_user, roles=['admin'])
    if not search_user:
        return HTTPException(status_code=400, detail=errors.ERR_CHECK_YOUR_TYPE)
    return search_user


@user_router.delete("/{delete_by_id}", dependencies=[Depends(cookie)], status_code=200)
def delete_user(delete_user, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    user = User.get_by_id(id=delete_user)
    if not user:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    db.delete(user)
    db.commit()
    return {}

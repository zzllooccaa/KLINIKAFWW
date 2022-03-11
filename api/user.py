from fastapi import APIRouter, Depends, HTTPException
from model import User, db
import schemas
from uuid import uuid4

from examples import user_example
from utils import auth_user, get_user_from_header
from fastapi_pagination import LimitOffsetPage, Page

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


@user_router.put('/logout')
def del_session(current_user: User = Depends(get_user_from_header)):
    _update_user_session(user=current_user, session_id=None)
    return {}


@user_router.post("/create_user")
def create_user(item: schemas.RegisterUser = user_example, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    if User.check_user_by_email(email=item.email):
        return HTTPException(status_code=400, detail=errors.ERR_USER_ALREADY_EXIST)
    if User.check_user_by_jmbg(email=item.jmbg):
        return HTTPException(status_code=400, detail=errors.ERR_USER_JMBG_ALREADY_EXIST)

    try:
        user = User(
            email=item.email,
            password=item.password,
            name=item.name,
            role=item.role,
            jmbg=item.jmbg
        )
        db.add(user)
        db.commit()
        return user

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@user_router.get("/users/", response_model=Page , status_code=200)
def get_user_by_id(by_id: str = None, name: str = None, by_role: str = None, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    return User.get_search_user(by_ids=by_id, names=name, by_roles=by_role)


# @user_router.get("/user/{user_id}", status_code=200)
# def get_user_by_id(user_id, current_user: User = Depends(get_user_from_header)):
#     auth_user(user=current_user, roles=['admin'])
#     return User.get_by_id(id=user_id)


@user_router.patch("/user/{user_id}", status_code=200)
def edit(user_id: int, user_data: schemas.UserUpdate, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    user_db = User.get_by_id(id=user_id)
    if not user_db:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    user_data_dic = user_data.dict(exclude_none=True)
    if user_data_dic['email'] == User.email:
        return errors
    user_data_dic = user_data.dict(exclude_none=True)
    User.edit_user(user_id=user_id, user_data=user_data_dic)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


# @user_router.get("/all_users", status_code=200)
# def get_all_user(email: str = None, name: str = None,
#                  current_user: User = Depends(get_user_from_header)):
#     auth_user(user=current_user, roles=['admin'])
#     users = User.get_all_user_paginate(email=email, name=name)
#     print(users[0].role)
#     return users


# @user_router.get("/{users_by_role}", status_code=200)
# def get_user_by_role(user_by_role, current_user: User = Depends(get_user_from_header)):
#     search_user = User.check_user_by_role(role=user_by_role)
#     auth_user(user=current_user, roles=['admin'])
#     if not search_user:
#         return HTTPException(status_code=400, detail=errors.ERR_CHECK_YOUR_TYPE)
#     return search_user


@user_router.patch("/{user_id}", status_code=200)
def delete_user(user_id, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    user = User.get_by_id(id=user_id)
    if not user:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    user.deleted = True
    db.add(user)
    db.commit()

    return {}

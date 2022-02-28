from fastapi import APIRouter, FastAPI, Response
from model import User, db
import schemas
from uuid import uuid4
from sessions.session_backends import backend as test

import errors



user_router = APIRouter()


@user_router.post("/login")
def login(item: schemas.UserLogin):
    user = User.get_user_by_email_and_password(email=item.email, password=item.password)
    if not user:
        return {"ERROR": errors.WRONG_CREDENTIALS}

    session = uuid4()
    data = schemas.SessionData(
        username=user.name,
        role=user.role,
        id=user.id
    )
    test.create(session, data)
    print(data)
    # cookie.attach_to_response(response, session)
    return user


@user_router.post("/create")
def create_user(item: schemas.UserRegisterLogin):
    if User.check_user_by_email(email=item.email):
        return errors.ERR_USER_ALREADY_EXIST

    if User.check_user_by_jmbg(jmbg=item.jmbg):
        return errors.ERR_USER_JMBG_ALREADY_EXIST
    # Provera da li email ili jmbg vec postoji u bazi
    # Pogledaj kako se radi or_ filter u sqlalchemy-ju
    print('item', item)
    try:
        user = User(
            email=item.email,
            password=item.password,
            name=item.name,
            surname=item.surname,
            jmbg=item.jmbg
        )
        db.add(user)
        db.commit()
        return user

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@user_router.patch("/{user_id}", status_code=200)
def edit(user_id, user_data: schemas.BaseUserSchema):
    user = User.get_user_by_id(id=user_id)
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


@user_router.get("/all_users")
def get_all_user(email: str = None, name: str = None, surname: str = None):
    users = User.get_all_user_paginate(email=email, name=name, surname=surname)
    # for user in users:
    #     print(users.name)
    # posts = User.query.order_by(User.time.desc()).paginate(page, per_page, error_out=False)
    return users

# all_user(user_data: schemas.UserSchema):
# users = User.get_all_user()
# return users

# users =User.get_all_user(id=item.id, name=item.name, surname=item.surname, jmbg=item.jmbg, email=item.email, address=item.addsress, phone=item.phone)
# for user in users:
# print(user)
# print(user.id, user.email)

# Pogledaj paginate sqlalchemy i vidi kako da vratis 10 korisnika iz prve strane

# Add filter LIKE in sqlaalchemy
# jedan poziv koji ce  mi vratiti sve korisnike ili recimo prvih 10

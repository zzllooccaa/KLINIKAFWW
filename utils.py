from starlette import status

import errors
from fastapi import HTTPException, Header
from model import User


def get_user_from_header(session_id: str = Header(None)):
    if session_id:
        # Ger from db by session_id
        user = User.get_by_session_id(session_id)
        if user:
            return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized"
    )


def auth_user(user, roles):
    """if"""
    if user.role.name not in roles:
        raise HTTPException(status_code=404, detail=errors.ERR_USER_NOT_GRANTED)

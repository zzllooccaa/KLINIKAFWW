import errors
from fastapi import HTTPException


def auth_user(user, roles):
    """if"""
    if user.role.name not in roles:
        raise HTTPException(status_code=404, detail=errors.ERR_USER_NOT_GRANTED)

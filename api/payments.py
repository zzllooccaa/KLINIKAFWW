from fastapi import APIRouter, Depends
from model import Payments, db, Role

from sess.sess_verifier import SessionData, verifier
from sess.sess_fronted import cookie

import errors

payments_router = APIRouter()


@payments_router.get("/all_payments", dependencies=[Depends(cookie)])
def get_all_payments(paid: str = None, session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.finance.name:
        return errors.ERR_USER_NOT_GRANTED

    lists = Payments.get_all_payments(paid=paid)
    return lists.all()

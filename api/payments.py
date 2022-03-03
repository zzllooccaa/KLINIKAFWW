from fastapi import APIRouter, Depends

import schemas
from model import Payments, db, Role

from sess.sess_verifier import SessionData, verifier
from sess.sess_fronted import cookie

import errors

payments_router = APIRouter()


@payments_router.get("/all_payments", dependencies=[Depends(cookie)])
def get_all_payments(all_paids: str = None, session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.finance.name:
        return errors.ERR_USER_NOT_GRANTED
    lists = Payments.get_all_payments(paid=all_paids)
    return lists.all()


# @payments_router.post("/create", dependencies=[Depends(cookie)])
# def create_payments(item: schemas.PaymentsSchema, session_data: SessionData = Depends(verifier)):
#     if session_data.role.name != Role.finance.name:
#         return errors.ERR_USER_NOT_GRANTED
#
#     try:
#         payments = Payments(
#             review_id=item.review_id,
#             customers_id=item.customers_id,
#             user_id=item.user_id,
#             price_list_id=item.price_list_id,
#             price_of_service=item.price_of_service,
#             paid=item.paid,
#             payment_made=item.payment_made,
#             finance_id=item.finance_id
#
#         )
#         db.add(payments)
#         db.commit()
#         return payments
#     except Exception as e:
#         db.rollback()
#         print(e)
#         return {'ERROR': 'ERR_DUPLICATED_ENTRY'}

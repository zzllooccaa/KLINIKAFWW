from fastapi import APIRouter, Depends, HTTPException

import schemas
from model import db, Review, User
from examples import payments_example

from utils import auth_user, get_user_from_header

import errors
import datetime

from fastapi_pagination import LimitOffsetPage, Page

payments_router = APIRouter()


@payments_router.patch("/create/{review_id}")
def create_payment(review_id, item: schemas.NewPayments = payments_example,
                   current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['finance'])
    review_check = Review.get_by_id(id=review_id)
    if not review_check:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)

    try:
        payments = Review(
            finance_id=current_user.id,
            paid=item.paid,
            payment_made=item.payment_made,
            date_of_creation_payment=datetime.datetime.now()
        )
        db.add(payments)
        db.commit()
        return payments
    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@payments_router.get("/get_all_payments/", response_model=Page)
#@payments_router.get("/get_all_review/limit-offset", response_model=LimitOffsetPage)
def get_all_payments(item: str = None, byid: int = None, paid: bool = None,  current_user: User = Depends(get_user_from_header)):#schemas.PaymentSearch,
    auth_user(user=current_user, roles=['finance'])
    review_check = Review.search_payments(name=item, id=byid, paid=paid)
    return review_check

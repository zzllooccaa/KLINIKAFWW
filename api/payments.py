from fastapi import APIRouter, Depends, HTTPException

import schemas
from model import db, Review, User
from examples import payments_example

from utils import auth_user, get_user_from_header

import errors
import datetime

from fastapi_pagination import Page, LimitOffsetPage

payments_router = APIRouter()


# @payments_router.get("/get_all_payments", response_model=LimitOffsetPage[schemas.PaymentSchema])
# def get_all_payments(current_user: User = Depends(get_user_from_header)):
#     auth_user(user=current_user, roles=['finance'])
#     print(current_user.role)
#     return Review.get_review_paginate()  #
#
#
# @payments_router.get("/{name}")
# def get_payments_by_doctor(name: str = None,
#                            current_user: User = Depends(get_user_from_header)):
#     auth_user(user=current_user, roles=['finance'])
#     return Review.get_review_by_doctor_paginate(name=name)  #
#
#
# @payments_router.get("/get_all_payments/paid", \
#                      response_model=LimitOffsetPage[schemas.PaymentSchema])
# def get_paid_review(current_user: User = Depends(get_user_from_header)):
#     auth_user(user=current_user, roles=['finance'])
#     print(current_user.role)
#     return Review.get_review_paid()
#
#
# @payments_router.get("/get/{review_id}")
# def get_one_payment(review_id, current_user: User = Depends(get_user_from_header)):
#     print(current_user.role)
#     auth_user(user=current_user, roles=['finance'])
#     print(current_user.role)
#     review_check = Review.get_review_by_id_paginate(byid=review_id)
#     if not review_check:
#         return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
#     return review_check  #


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


@payments_router.get("/payments/get_all_payments/{name}",
                     response_model=LimitOffsetPage[schemas.PaymentSchema])
def get_all_payments(name: str = None, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['finance'])
    a = Review.get_payment_by_doctor_paginate(name=name)
    return a
    if not a:
     review_check = Review.get_review_by_id_paginate(byid=name)
    return review_check
    if not review_check:
        b = Review.get_review_paid()
        return b
    if not b:
        return Review.get_review_paginate()

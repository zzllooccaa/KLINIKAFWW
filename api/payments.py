from fastapi import APIRouter, Depends, HTTPException

import schemas
from model import db, Review, User
from examples import payments_example

from utils import auth_user, get_user_from_header

import errors
import datetime

from fastapi_pagination import Page, LimitOffsetPage

payments_router = APIRouter()


@payments_router.get("/get_all_review", response_model=Page[schemas.PaymentSchema])
@payments_router.get("/get_all_review/limit-offset", response_model=LimitOffsetPage[schemas.PaymentSchema])
def get_all_review(current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['finance'])
    print(current_user.role)
    return Review.get_review_paginate()


@payments_router.get("/get/{review_id}")
def get_one_payment(review_id, current_user: User = Depends(get_user_from_header)):
    print(current_user.role)
    auth_user(user=current_user, roles=['finance'])
    print(current_user.role)
    review_check = Review.get_review_by_id_paginate(byid=review_id)
    if not review_check:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    return review_check


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

# @payments_router.post("/create", dependencies=[Depends(cookie)])
# def create_review(item: schemas.PaymentsSchema, session_data: SessionData = Depends(verifier)):
#############################################################
# CHECK user role. If user is not doctor, then return error. #
#############################################################
# if session_data.role.name != Role.finance.name:
#     return errors.ERR_USER_NOT_GRANTED
#
# customer = model.Customers.get_by_id(id=item.customers_id)
# if not customer:
#     return errors.ERR_ID_NOT_EXIST
# price = model.PriceList.get_by_id(id=item.price_list_id)
# if not price:
#     return errors.ERR_ID_NOT_EXIST

# try:
#     payments = Payments(
#         review_id=Review.id,
#         user_id=Review.doctor_id,
#         price_list_id=PriceList.id,
#         price_of_service=Review.price_of_service,
#         customers_id=Review.customers_id,
#         paid=item.paid,
#         payment_made=item.payment_made,
#         finance_id=session_data.id
#     )
#     db.add(payments)
#     db.commit()
#     return payments
# except Exception as e:
#     db.rollback()
#     print(e)
#     return {'ERROR': 'ERR_DUPLICATED_ENTRY'}
#
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

from fastapi import APIRouter, Depends
import model
import schemas
from model import db, Role, Customers, PriceList, User, Review
from utils import auth_user

from sess.sess_verifier import SessionData, verifier
from sess.sess_fronted import cookie

import errors
import datetime

payments_router = APIRouter()


@payments_router.get("/get_all_review", dependencies=[Depends(cookie)])
def get_all_review(session_data: SessionData = Depends(verifier)):
    auth_user(user=session_data, roles=['finance'])
    review = Review.get_review_all()
    return review


@payments_router.get("/create/{review_id}", dependencies=[Depends(cookie)])
def create_payment(review_id, session_data: SessionData = Depends(verifier)):
    auth_user(user=session_data, roles=['finance'])
    review_check = Review.get_review_by_id_paginate(byid=review_id)
    if not review_check:
        return errors.ERR_ID_NOT_EXIST
    return review_check


@payments_router.patch("/create/{review_id}", dependencies=[Depends(cookie)])
def create_payment(review_id, item: schemas.NewPayments, session_data: SessionData = Depends(verifier)):
    auth_user(user=session_data, roles=['finance'])
    review_check = Review.get_by_id(id=review_id)
    if not review_check:
        return errors.ERR_ID_NOT_EXIST

    try:
        payments = Review(
            finance_id=session_data.id,
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

from fastapi import APIRouter, Depends
from sqlalchemy import join

import model
import schemas
from model import Review, Role, db, ReviewDocument

import errors
from sess.sess_fronted import cookie

from sess.sess_verifier import SessionData, verifier

review_router = APIRouter()


@review_router.post("/create", dependencies=[Depends(cookie)])
def create_review(item: schemas.NewReview, session_data: SessionData = Depends(verifier)):
    ##############################################################
    # CHECK user role. If user is not doctor, then return error. #
    ##############################################################
    if session_data.role.name != Role.doctor.name:
        return errors.ERR_USER_NOT_GRANTED

    customer = model.Customers.get_by_id(id=item.customers_id)
    if not customer:
        return errors.ERR_ID_NOT_EXIST
    price = model.PriceList.get_by_id(id=item.price_list_id)

    try:
        review = Review(
            doctor_opinion=item.doctor_opinion,
            price_of_service=item.price_of_service,
            doctor_id=session_data.id,
            customers_id=customer.id,
            price_list_id=price.id
        )
        db.add(review)
        db.commit()
        return review
    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@review_router.get("/get_review/{name}", dependencies=[Depends(cookie)])
def get_all_review(name: str = None, session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.doctor.name:
        return errors.ERR_USER_NOT_GRANTED
    review = Review.get_review_by_name_paginate(name=name)
    return review


# @review_router.post("/upload_file")
# def create_upload_file(file: ReviewDocument):
#     return {"filename": file.url}

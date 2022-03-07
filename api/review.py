from fastapi import APIRouter, Depends  # , File, UploadFile


import model
import schemas
from model import Review, db, Customers
from utils import auth_user

import errors
from sess.sess_fronted import cookie

from sess.sess_verifier import SessionData, verifier

review_router = APIRouter()


@review_router.post("/create", dependencies=[Depends(cookie)])
def create_review(item: schemas.NewReview, session_data: SessionData = Depends(verifier)):
    auth_user(user=session_data, roles=['doctor'])
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


@review_router.get("/get_all_review", dependencies=[Depends(cookie)])
def get_all_review(session_data: SessionData = Depends(verifier)):
    auth_user(user=session_data, roles=['doctor'])
    return Review.get_review_all()


@review_router.get("/all_review_customers/{name}", dependencies=[Depends(cookie)])
def get_review_all_customer(name: str = None,
                            session_data: SessionData = Depends(verifier)):
    auth_user(user=session_data, roles=['doctor'])
    return Customers.get_review_by_name_paginate(name=name)


# @review_router.post("/upload_file")
# def create_file(file: bytes = File(...)):
#     return {"file_size": len(file)}

# @review_router.post("/upload_file")
# def create_upload_file(file: ReviewDocument):
#     return {"filename": file.url}

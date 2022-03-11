from fastapi import APIRouter, Depends
import model
import schemas

from model import Review, db, Customers, User
from utils import auth_user, get_user_from_header

import errors


review_router = APIRouter()


@review_router.post("/create")
def create_review(item: schemas.NewReview, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    customer = model.Customers.get_by_id(id=item.customers_id)
    if not customer:
        return errors.ERR_ID_NOT_EXIST
    price = model.PriceList.get_by_id(id=item.price_list_id)

    try:
        review = Review(
            doctor_opinion=item.doctor_opinion,
            price_of_service=item.price_of_service,
            doctor_id=current_user.id,
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


#@review_router.get("/get_all_review2")
# def get_all_review(current_user: User = Depends(get_user_from_header)):
    # auth_user(user=current_user, roles=['doctor'])
    # return Review.get_review_all()


@review_router.get("/all_review_review")
def get_review_all_customer(name: str = None, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    return Customers.get_review_by_name_paginate(name=name)

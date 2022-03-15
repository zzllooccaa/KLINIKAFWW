from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, responses
import model
from deta import Drive
import schemas
import images
import shutil
from fastapi.staticfiles import StaticFiles


from model import Review, db, Customers, User, ReviewDocument
from utils import auth_user, get_user_from_header

import errors

from typing import Optional

review_router = APIRouter()
#files = Drive("images")



@review_router.post("/create")
def create_review(file: Optional[UploadFile] = File(...),
                  customer_id: int = Form(...),
                  price_list_id: int = Form(...),
                  doctor_opinion: Optional[str] = Form(None),
                  price_of_service: Optional[int] = Form(None),
                  current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    customer = model.Customers.get_by_id(id=customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)

    price = model.PriceList.get_by_id(id=price_list_id)
    if not price:
        raise HTTPException(status_code=400, detail=errors.WRONG_CREDENTIALS)

    try:
        review = Review(
            doctor_id=current_user.id,
            customers_id=customer_id,
            price_list_id=price_list_id,
            doctor_opinion=doctor_opinion,
            price_of_service=price_of_service
        )
        db.add(review)
        db.flush()

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}

    if file:
        with open("images/" + file.filename, 'wb') as image:
            shutil.copyfileobj(file.file, image)
            try:
                review_document = ReviewDocument(
                    url=("images/" + file.filename),
                    title=file.filename,
                    review_id=review.id

                )

                db.add(review_document)
                return {"file_name": file.filename}
            except Exception as e:
                db.rollback()
                print(e)
                return {'ERROR': 'ERR_DUPLICATED_ENTRY'}

    db.commit()
    db.refresh()
    return review  # ovde treba ubaciti upload file-a pa tek nakon toga return


# @review_router.get("/get_all_review2")
# def get_all_review(current_user: User = Depends(get_user_from_header)):
# auth_user(user=current_user, roles=['doctor'])
# return Review.get_review_all()


@review_router.get("/all_review_review")
def get_review_all_customer(name: str = None, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    return Customers.get_review_by_name_paginate(name=name)


@review_router.get("/{review_id}")
def get_file_of_review(rev_id, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    review = Review.get_by_id(id=rev_id)
    setattr(review, 'documents', ReviewDocument.get_review_by_id(id=rev_id))  # review.documents
    return review

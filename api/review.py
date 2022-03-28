import datetime
import string

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from model import Review, db, Customers, User, ReviewDocument
from fastapi.responses import FileResponse
from utils import auth_user, get_user_from_header
from config import path_images
from typing import Optional
import random

import shutil
import model
import schemas
import errors


review_router = APIRouter()


@review_router.post("/create")
def create_review(file: Optional[UploadFile] = File(None),
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
        db.commit()

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}

    if file:
        a = random.choice(string.digits)
        b = datetime.datetime.now()
        c= b.strftime("%H:%M:%S") + a
        name_hash = c + file.filename
        #with open(path_images + f'/{file.filename}', 'wb') as image:
        with open(path_images + f'/{name_hash}', 'wb') as image:
            shutil.copyfileobj(file.file, image)
            try:
                review_document = ReviewDocument(
                    url=(path_images + name_hash),
                    title=name_hash,
                    review_id=review.id

                )

                db.add(review_document)
                db.commit()
                return {"file_name": name_hash}
            except Exception as e:
                db.rollback()
                print(e)
                return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


    return review


@review_router.get("/{review_id}")
def get_file_of_review(rev_id, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    return schemas.ReviewResponseSchema().dump(Review.get_by_id(id=rev_id), many=False)


@review_router.get("/customer/{customer_id}")
def get_review_by_customer(cus_id, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    return schemas.ReviewCustomersResponseSchema().dump(Customers.get_by_id(id=cus_id), many=False)


@review_router.get("/download/{name_file}")
def download_file(name_file: str, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    return FileResponse \
        (path=path_images + "/" + name_file, \
         media_type='application/octet-stream', filename=name_file)

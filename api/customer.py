import shutil
import images
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Path, File
from fastapi_pagination import Page
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import paginate

from model import Customers, db, User
import schemas

from utils import auth_user, get_user_from_header

import errors

customer_router = APIRouter()


@customer_router.post("/create_patient")
def create_customer(item: schemas.AddCustomer, \
                    current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    if Customers.check_customer_by_email(email=item.email):
        return HTTPException(status_code=400, detail=errors.ERR_CUSTOMER_ALREADY_EXIST)
    try:
        customers = Customers(
            email=item.email,
            date_of_birth=item.date_of_birth,
            personal_medical_history=item.personal_medical_history,
            family_medical_history=item.family_medical_history,
            company_name=item.company_name,
            company_pib=item.company_pib,
            company_address=item.company_address,
            name=item.name,
            jmbg=item.jmbg,
            address=item.address,
            phone=item.phone
        )
        db.add(customers)
        db.commit()
        print(customers)
        return customers

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@customer_router.get("/all_customers/", response_model=Page)
def get_all_customer(name: str = None, byid: int = None, by_jmbg: int = None,
                     current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    return Customers.get_customer_by_name_paginate(name=name, byid=byid, by_jmbg=by_jmbg)


@customer_router.patch("/{edit_by_id}")
def edit(edit_by_id, customer_data: schemas.CustomerUpdate,
         current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    customer = Customers.get_id(ide=edit_by_id)
    if not customer:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)

    customer_d = customer_data.dict(exclude_none=True)
    Customers.edit_customer(custom_id=edit_by_id, customer_data=customer_d)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@customer_router.get("/search/{search_by_id}")
def search(search_by_id, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    return schemas.CustomersResponseSchema() \
        .dump(Customers.get_by_id(id=search_by_id), many=False)

# @customer_router.post("upload_file/{customer_id}")
# async def post(customer_id: int, file: UploadFile = File(...)):
#     print(file, file.filename)
#     with open("images//" + file.filename, 'wb') as image:
#         shutil.copyfileobj(file.file, image)
#         return {"file_name": file.filename}
#        content = file.read()
# image.write(content)
# image.close()
# return {}

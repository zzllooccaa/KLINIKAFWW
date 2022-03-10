from fastapi import APIRouter, Depends, HTTPException
from model import Customers, db, User
import schemas

from utils import auth_user, get_user_from_header
from examples import customer_example

import errors

customer_router = APIRouter()


@customer_router.post("/create_patient")
def create_customer(item: schemas.AddCustomer, current_user: User = Depends(get_user_from_header)):  # , session_data: SessionData = Depends(verifier)):
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


@customer_router.get("/all_customers/{name}")
def get_all_customer(name: str = None,
                     current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    return Customers.get_customers_by_name_paginate(name=name)


@customer_router.get("/all_customers")
def get_review_all_customer(current_user: User = Depends(get_user_from_header)):
    # Check user permissions
    auth_user(user=current_user, roles=['doctor'])
    return Customers.get_all_customers()


@customer_router.patch("/{edit_by_id}")
def edit(edit_by_id, customer_data: schemas.CustomerUpdate,
         current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    customer = Customers.get_by_id(id=edit_by_id)
    if not customer:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)

    customer_d = customer_data.dict(exclude_none=True)
    for key, value in customer_d.items():
        setattr(customer[0], key, value)
    db.add(customer[0])
    db.commit()
    db.refresh(customer[0])
    return customer


@customer_router.get("/search-customer/{customer_jmbg}")
def search(customer_jmbg, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['doctor'])
    search_customer = Customers.get_customer_by_jmbg(jmbg=customer_jmbg)
    if not search_customer:
        return HTTPException(status_code=400, detail=errors.ERR_JMBG_NOT_EXIST)
    return search_customer

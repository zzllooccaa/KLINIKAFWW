from fastapi import APIRouter, Depends
from model import Customers, db, Role
import schemas
from sess.sess_fronted import cookie
from sess.sess_verifier import SessionData, verifier
from typing import Optional

import errors

customer_router = APIRouter()


@customer_router.post("/create_patient", dependencies=[Depends(cookie)])
def create_customer(item: schemas.AddCustomer, session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.doctor.name:
        return errors.ERR_USER_NOT_GRANTED
    if Customers.check_customer_by_email(email=item.email):
        return errors.ERR_CUSTOMER_ALREADY_EXIST

    # if Customers.check_customer_by_jmbg(jmbg=item.jmbg):
    #     return errors.ERR_CUSTOMER_JMBG_ALREADY_EXIST

    try:
        customer = Customers(
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
        db.add(customer)
        db.commit()
        return customer

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@customer_router.get("/all_customers/{name}", dependencies=[Depends(cookie)])
def get_all_customer(name: str = None,
                     session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.doctor.name:
        print(session_data.role.name)
        print(Role.doctor.name)
        return errors.ERR_USER_NOT_GRANTED
    print(name)
    customers = Customers.get_all_customer_paginate(name=name)
    return customers


@customer_router.get("/all_customers", dependencies=[Depends(cookie)])
def get_review_all_customer(session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.doctor.name:
        return errors.ERR_USER_NOT_GRANTED
    customers = Customers.get_all_customers()
    return customers


@customer_router.patch("/{edit_by_id}", dependencies=[Depends(cookie)], status_code=200)
def edit(edit_by_id, customer_data: schemas.CustomerUpdate,
         session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.admin.name:
        return errors.ERR_USER_NOT_GRANTED
    customer = Customers.get_by_id(id=edit_by_id)
    if not customer:
        return errors.ERR_ID_NOT_EXIST

    customer_d = customer_data.dict(exclude_none=True)
    for key, value in customer_d.items():
        setattr(customer[0], key, value)
    db.add(customer[0])
    db.commit()
    db.refresh(customer[0])
    return customer
    # try:
    # Customers.edit_customer(customer_id=edit_by_id, customer_data=customer_data_dict)
    # db.add(customer)
    # db.commit()

    # except Exception as e:
    # if 'duplicate key value violates unique constraint' in str(e):
    # return {"ERROR": "ERR_DUPLICATED_ENTRY"}


# return {}


@customer_router.get("/search-customer/{customerjmbg}", status_code=200)
def search(customerjmbg):
    search_customer = Customers.get_customer_by_jmbg(jmbg=customerjmbg)
    if not search_customer:
        return errors.ERR_JMBG_NOT_EXIST
    print(search_customer)
    return search_customer

from fastapi import APIRouter, Depends
from model import Customers, db, Role
import schemas
from sess.sess_fronted import cookie
from sess.sess_verifier import SessionData, verifier

import errors

customer_router = APIRouter()


@customer_router.post("/create", dependencies=[Depends(cookie)])
def create_customer(item: schemas.AddCustomer, session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.admin.name:
        return errors.ERR_USER_NOT_GRANTED
    if Customers.check_customer_by_email(email=item.email):
        return errors.ERR_CUSTOMER_ALREADY_EXIST

    if Customers.check_customer_by_jmbg(jmbg=item.jmbg):
        return errors.ERR_CUSTOMER_JMBG_ALREADY_EXIST

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
            surname=item.surname,
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


@customer_router.get("/all_customers", dependencies=[Depends(cookie)])
def get_all_customer(email: str = None, name: str = None, surname: str = None,
                     session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.doctor.name:
        return errors.ERR_USER_NOT_GRANTED
    customers = Customers.get_all_customer_paginate(email=email, name=name, surname=surname)
    return customers


@customer_router.patch("/{customer_id}", status_code=200)
def edit(customer_id, customer_data: schemas.BaseUserSchema):
    customer = Customers.get_by_id(id=customer_id)
    if not customer:
        return {"ERROR": "User id not exist"}

    customer_data_dict = customer_data.dict(exclude_none=True)
    try:
        Customers.edit_customer(customer_id=customer_id, customer_data=customer_data_dict)
        db.add(customer)
        db.commit()

    except Exception as e:
        if 'duplicate key value violates unique constraint' in str(e):
            return {"ERROR": "ERR_DUPLICATED_ENTRY"}

        return {"ERROR": "ERR_CANNOT_EDIT_USER"}

    return customer


@customer_router.get("/search-customer/{customer_jmbg}", status_code=200)
def search(customer_jmbg):
    search_customer = Customers.get_customer_by_jmbg(jmbg=customer_jmbg)
    if not search_customer:
        return errors.ERR_USER_NOT_GRANTED
    print(search_customer)
    return search_customer
# Todo search customer ruta koja ce po jmbg da nadje customera

from fastapi import APIRouter, Depends, HTTPException
from model import PriceList, db, User
import schemas
import datetime
from helper import create_new_price
from examples import price_list_example
from utils import auth_user, get_user_from_header

import errors

price_list_router = APIRouter()


@price_list_router.post("/create")
def create_price_list(item: schemas.AddPriceList ,
                      current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])

    try:
        return create_new_price(item=item)

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@price_list_router.get("/all_prices")
def get_all_price(services: str = None, medical_service: str = None,
                  current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin', 'doctor'])
    return PriceList.get_all_price(services=services, medical_service=medical_service, )  # Todo dateofendd=null


@price_list_router.patch("/edit/{pricelist_id}")
def edit_price(price_list_id, pricelist_data: schemas.PriceListSchema,
               current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    price_list = PriceList.get_by_id(id=price_list_id)
    if not price_list:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    pricelist_data_dict = pricelist_data.dict(exclude_none=True)

    ##################################################################################################
    # AKO SE MENJA CENA STAVI END DATE U CENOVNIKU NA TU USLUGU I KREIRAJ  NOVU USLUGU BEZ ENDDATE-A #
    ##################################################################################################
    if pricelist_data_dict['price_of_service'] != price_list.price_of_service:
        price_list.date_of_end = datetime.datetime.now()
        db.add(price_list)
        db.commit()

        price_list = create_new_price(item=pricelist_data)

    else:
        PriceList.edit_price_list(price_list_id=price_list_id, pricelist_data=pricelist_data_dict)
        db.add(price_list)
        db.commit()

    return price_list


@price_list_router.patch("/delete/{price_list_id}")
def delete_price(price_list_id, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['admin'])
    price = PriceList.get_by_id(id=price_list_id)
    if not price:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)
    price.date_of_end = datetime.datetime.now()
    db.add(price)
    db.commit()
    return {}

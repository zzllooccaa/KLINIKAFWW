from fastapi import APIRouter, Depends
from model import PriceList, db, Role
import schemas
import datetime
from helper import create_new_price
from sess.sess_verifier import SessionData, verifier
from sess.sess_fronted import cookie

import errors

price_list_router = APIRouter()


@price_list_router.post("/create", dependencies=[Depends(cookie)])
def create_price_list(item: schemas.AddPriceList, session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.admin.name:
        return errors.ERR_USER_NOT_GRANTED

    try:
        price_list = create_new_price(item=item)

        return price_list

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@price_list_router.get("/all_prices", dependencies=[Depends(cookie)])
def get_all_price(service: str = None, medical_service: str = None, session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.admin.name:
        return errors.ERR_USER_NOT_GRANTED

    lists = PriceList.get_all_price(service=service, medical_service=medical_service, )  # Todo dateofendd=null

    return lists


@price_list_router.patch("/edit/{pricelist_id}", dependencies=[Depends(cookie)])
def edit_price(price_list_id, pricelist_data: schemas.PriceListSchema, session_data: SessionData = Depends(verifier)):
    if session_data.role.name != Role.admin.name:
        return errors.ERR_USER_NOT_GRANTED

    price_list = PriceList.get_by_id(id=price_list_id)
    if not price_list:
        return errors.ERR_ID_NOT_EXIST
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

    return price_list

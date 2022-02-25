from fastapi import APIRouter
from model import PriceList, db
import schemas

import errors

price_list_router = APIRouter()


@price_list_router.post("/create")
def create_price_list(item: schemas.AddPriceList):
    if PriceList.check_price_list_by_medical_service(medical_service=item.medical_service):
        return errors.ERR_PRICE_LIST_EXIST

    try:
        price_list = PriceList(
            services=item.services,
            medical_service=item.medical_service,
            price_of_service=item.price_of_service,
            time_for_exam=item.time_for_exam
        )
        db.add(price_list)
        db.commit()
        return price_list

    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@price_list_router.get("/all_prices")
def get_all_price(service: str = None, medical_service: str = None):
    lists = PriceList.get_all_price(service=service, medical_service=medical_service)
    # for user in users:
    #     print(users.name)
    # posts = User.query.order_by(User.time.desc()).paginate(page, per_page, error_out=False)
    return lists

from model import PriceList, db


def create_new_price(item):
    price_list = PriceList(
        services=item.services,
        medical_service=item.medical_service,
        price_of_service=item.price_of_service,
        time_for_exam=item.time_for_exam
    )
    db.add(price_list)
    db.commit()
    return price_list

#

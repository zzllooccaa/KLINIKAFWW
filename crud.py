from sqlalchemy.orm import Session
from model import Review, ReviewDocument, User, BaseUser, BaseModels, Payments, PriceList, Customers

from schemas import ReviewSchema, ReviewDocumentSchema, BaseUserSchema, BaseModelsSchema, \
    PaymentsSchema, PriceListSchema, CustomersSchema, UserSchema


#def create_role(db: Session, role: RoleSchema):
   # _role = Role(admin=role.admin, doctor=role.doctor, finance=role.finance)
    #db.add(_role)
    #db.commit()
    #db.refresh(_role)
    #return _role


#def create_pays(db: Session, pays: PaysSchema):
    #_pays = Pays(cash=pays.cash, card=pays.card, cash_card=pays.cash_card)
    #db.add(_pays)
    #db.commit()
    #db.refresh(_pays)
    #return _pays


def create_review(db: Session, review: ReviewSchema):
    _review = Review(price_of_service=review.price_of_service, doctor_opinion=review.doctor_opinion)
    db.add(_review)
    db.commit()
    db.refresh(_review)
    return _review


def create_review_document(db: Session, review_document: ReviewDocumentSchema):
    _review_document = ReviewDocument(url=review_document.url, title=review_document.title)
    db.add(_review_document)
    db.commit()
    db.refresh(_review_document)
    return _review_document


def create_user(db: Session, create_user: UserSchema):
    _user = User(password=create_user.password, role=create_user.role)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def create_base_user(db: Session, create_base_user: BaseUserSchema):
    _base_user = BaseUser(name=create_base_user.name, surname=create_base_user.surname, jmbg=create_base_user.jbmg,
                          email=create_base_user.email, address=create_base_user.address, phone=create_base_user.phone)
    db.add(_base_user)
    db.commit()
    db.refresh(_base_user)
    return _base_user


def create_base_models(db: Session, create_base_models: BaseModelsSchema):
    _base_models = BaseModels(date_of_creation=create_base_models.date_of_creation)
    db.add(_base_models)
    db.commit()
    db.refresh(_base_models)
    return _base_models


def create_payments(db: Session, create_payments: PaymentsSchema):
    _payments = Payments(price_of_service=create_payments.price_of_service, paid=create_payments.paid,
                         payment_made=create_payments.payment_made)
    db.add(_payments)
    db.commit()
    db.refresh(_payments)
    return _payments


def create_price_list(db: Session, create_price_list: PriceListSchema):
    _price_list = PriceList(services=create_price_list.services, medical_service=create_price_list.medical_service,
                            price_of_service=create_price_list.price_of_service,
                            time_for_exam=create_price_list.time_for_exam)
    db.add(_price_list)
    db.commit()
    db.refresh(_price_list)
    return _price_list


def create_customers(db: Session, create_customers: CustomersSchema):
    _customers = Customers(date_of_birth=create_customers.date_of_birth,
                           personal_medical_history=create_customers.personal_medical_history,
                           family_medical_history=create_customers.family_medical_history,
                           comany_name=create_customers.company_name, company_pib=create_customers.company_pib,
                           company_address=create_customers.company_address)
    db.add(_customers)
    db.commit()
    db.refresh(_customers)
    return _customers

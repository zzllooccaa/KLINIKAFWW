import simplejson
import os
import datetime
from _datetime import date
import enum
from json import JSONEncoder
from fastapi_pagination import paginate
from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from dataclasses import dataclass

DATABASE_URL = "postgresql://postgres:myPassword@localhost:5432/Clinic22"

engine = create_engine(
    DATABASE_URL, json_serializer=lambda obj: simplejson.dumps(obj)
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()
Base = declarative_base()

load_dotenv('.env')


########################################################
# export PYTHONPATH=.                                  #
# alembic upgrade head                                 #
# alembic revision --autogenerate -m "user_phone_add"  #
# alembic upgrade head                                 #
########################################################


##############################
# ENUM USER AND TYPE OFF PAY #
##############################


class Role(enum.Enum):
    admin = 'admin'
    doctor = 'doctor'
    finance = 'finance'


class Pays(enum.Enum):
    cash = 'cash'
    card = 'card'
    cash_card = 'cash_card'


class BaseModels(object):
    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True, autoincrement=True, unique=True)

    @declared_attr
    def date_of_creation(self):
        return Column(DateTime(), default=datetime.datetime.today())

    @classmethod
    def get_by_id(cls, id):
        return db.query(cls) \
            .filter(cls.id == id) \
            .first()

    @classmethod
    def get_id(cls, ide):
        return db.query(cls).filter(cls.id == ide).first()


class BaseUser(BaseModels):

    @declared_attr
    def name(self):
        return Column(String(255), nullable=False)

    @declared_attr
    def email(self):
        return Column(String, unique=True)

    @declared_attr
    def address(self):
        return Column(String(255))

    @declared_attr
    def phone(self):
        return Column(String(20))


@dataclass
class User(Base, BaseUser, JSONEncoder):
    __tablename__ = 'user'

    id: int
    email: str
    password: str
    address: str
    phone: str
    name: str
    session_id: str
    Role.role: str

    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.doctor)  # Enum polje
    session_id = Column(String(100))
    jmbg = Column(String, unique=True)
    deleted = Column(Boolean, default=False)
    hashed_password = Column(String(150))

    ########################
    # GET REVIEW BY DOCTOR #
    ########################

    # @classmethod
    # def get_review_by_doctor_paginate(cls, name):
    #     return db.query(cls) \
    #         .join(Review, Review.doctor_id == User.id) \
    #         .filter(User.name.ilike('%' + name + '%'), ~cls.deleted) \
    #         .options(joinedload(cls.reviews)) \
    #         .order_by(cls.date_of_creation).all()

    ################################
    # GET USER BY EMAIL & PASSWORD #
    ################################

    @classmethod
    def get_by_session_id(cls, session_id):
        return db.query(cls).filter(cls.session_id == session_id, ~cls.deleted).first()

    @classmethod
    def get_user_by_email_and_password(cls, email, password):
        return db.query(cls) \
            .filter(cls.email == email, cls.password == password, ~cls.deleted) \
            .first()

    @classmethod
    def get_user_by_email(cls, email):
        return db.query(cls) \
            .filter(cls.email == email, ~cls.deleted) \
            .first()

    @classmethod
    def get_user_recover(cls, hashed_password):
        return db.query(cls) \
            .filter(cls.hashed_password == hashed_password, ~cls.deleted) \
            .first()

    #################################################
    # GET ALL USER SEARCHED BY EMAIL,NAME & SURNAME #
    #################################################

    # @classmethod
    # def get_all_user_paginate(cls, email, name):
    #     users = db.query(cls).filter(~cls.deleted)
    #     if email:
    #         users = users.filter(cls.email == email, ~User.deleted)
    #     if name:
    #         users = users.filter(cls.name == name, ~User.deleted)
    #
    #     return users.all()

    #########################################
    # CHECK USER BY EMAIL , JMBG & AND ROLE #
    #########################################

    @classmethod
    def check_user_by_email(cls, email):
        return db.query(cls).filter(cls.email == email, ~User.deleted).first()

    @classmethod
    def check_user_by_jmbg(cls, jmbg):
        return db.query(cls).filter(cls.jmbg == jmbg, ~User.deleted).first()


    ##################
    # UPDATE METHODS #
    ##################
    @classmethod
    def edit_user(cls, user_id, user_data):
        print('USER DATA', user_data)
        return db.query(cls).filter(cls.id == user_id, ~cls.deleted) \
            .update(user_data, synchronize_session=False)

    @classmethod
    def forgot_user(cls, email, user_data):
        db.query(cls).filter(cls.email == email, ~cls.deleted) \
            .update(user_data, synchronize_session=False)

    ##################
    # GET USER BY ID #
    ##################
    @classmethod
    def get_search_user(cls, names, by_ids, by_roles):
        users = db.query(cls)
        if names:
            users = users.filter(User.name.ilike('%' + names + '%'))
        if by_ids:
            users = users.filter(cls.id == by_ids)
        if by_roles:
            users = users.filter(cls.role == by_roles)

        return paginate(users.order_by(cls.date_of_creation).all())



class Customers(Base, BaseUser):
    __tablename__ = 'customers'

    id: int
    email: str
    password: str
    address: str
    phone: str
    name: str
    date_of_birth: date
    jmbg: str
    personal_medical_history: str
    family_medical_history: str
    company_name: str
    company_pib: str
    company_address: str

    date_of_birth = Column(DateTime, nullable=False)
    jmbg = Column(String)
    personal_medical_history = Column(Text)
    family_medical_history = Column(Text)
    company_name = Column(Text)
    company_pib = Column(String)
    company_address = Column(String)

    review = relationship('Review')

    ###################################
    # GET CUSTOMER BY NAME ID OR JMBG #
    ###################################

    @classmethod
    def get_customer_by_name_paginate(cls, name, byid, byjmbg):
        customs = db.query(cls)
        if name:
            return paginate(customs.filter(Customers.name.ilike('%' + name + '%')).all())
        if byid:
            return paginate(customs.filter(Customers.id == byid).all())
        if byjmbg:
            return paginate(customs.filter(Customers.jmbg == byjmbg).all())

        return paginate(customs.all())

    ###########################
    # CHECK CUSTOMER BY EMAIL #
    ###########################
    @classmethod
    def check_customer_by_email(cls, email):
        return db.query(cls).filter(cls.email == email, cls.email != None).first()


    #######################
    # EDIT CUSTOMER BY ID #
    #######################

    @classmethod
    def edit_customer(cls, custom_id, customer_data):
        db.query(cls).filter(cls.id == custom_id) \
            .update(customer_data, synchronize_session=False)



########################
# GET CUSTOMER BY NAME #
########################

# @classmethod
# def get_customers_by_name_paginate(cls, name):
#     customers = db.query(cls). \
#         filter(Customers.name.ilike('%' + name + '%')) \
#         .order_by(cls.date_of_creation).all()
#     return customers


####################
# GET ALL CUSTOMER #
####################

# @classmethod
# def get_all_customers(cls):
#     return db.query(cls).all()


##########################
# CHECK CUSTOMER BY JMBG #
##########################


#################
# EDIT CUSTOMER #
#################

# @classmethod
# def edit_customer(cls, customer_id, customer_data):
#     db.query(cls).filter(cls.id == customer_id).update(customer_data, synchronize_session=False)


class PriceList(Base, BaseModels):
    __tablename__ = 'price_list'

    services = Column(String)
    medical_service = Column(String)
    price_of_service = Column(Integer)
    time_for_exam = Column(Integer)
    date_of_end = Column(DateTime)

    ###########################
    # CHECK PRICE BY SERVICES #
    ###########################

    # @classmethod
    # def check_price_list_by_services(cls, services):
    #     return db.query(cls) \
    #         .filter(cls.services == services, cls.date_of_end == None) \
    #         .first()

    ###############################################
    # GET ALL PRICE'S AND SEARCH BY MODEL OR TYPE #
    ###############################################

    @classmethod
    def get_all_price(cls, services, medical_service):
        price_list = db.query(cls).filter(cls.date_of_end == None)
        if services:
            price_list = price_list.filter(cls.services == services)
        if medical_service:
            price_list = price_list.filter(cls.medical_service == medical_service)

        return price_list.all()

    ##############################
    # EDIT PRICE_LIST AND DELETE #
    ##############################

    @classmethod
    def edit_price_list(cls, price_list_id, pricelist_data):
        db.query(cls) \
            .filter(cls.id == price_list_id, cls.date_of_end == None) \
            .update(pricelist_data, synchronize_session=False)

    # @classmethod
    # def delete_by_id(cls, id):
    #     return db.query(cls).filter(cls.id == id).all()


class Review(Base, BaseModels):
    __tablename__ = 'review'

    title: str
    review_id: int
    url: str
    id: int

    customers_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    price_list_id = Column(Integer, ForeignKey('price_list.id'), nullable=False)
    price_of_service = Column(Integer)
    doctor_opinion = Column(Text)
    paid = Column(Boolean, default=False)  # True=paid , False = unpaid
    payment_made = Column(Enum(Pays), default=Pays.card)  # Enum cash, card or cash_card
    date_of_creation_payment = Column(DateTime)
    finance_id = Column(Integer, ForeignKey('user.id'))

    customers_a = relationship('Customers', viewonly=True)
    doctor_a = relationship('User', viewonly=True, foreign_keys="Review.doctor_id")
    price_list_a = relationship('PriceList', viewonly=True, foreign_keys="Review.price_list_id")
    documents = relationship("ReviewDocument", back_populates='review')

    # primaryjoin="ReviewDocument.review_id==review.c.id")

    # @classmethod
    # def get_review_all(cls):
    #     return db.query(cls).all()

    # @classmethod
    # def get_review_paginate(cls):
    #     return paginate(db.query(cls).all())

    #################################################
    # SEARCH PAYMENTS BY NAME BY ID OR PAID(UNPAID) #
    #################################################

    @classmethod
    def search_payments(cls, name, id, paid):
        payments = db.query(cls)
        if name:
            payments = payments.filter(User.name.ilike('%' + name + '%'))
        if id:
            payments = payments.filter(Review.id == id)
        if paid:
            payments = payments.filter(Review.paid == True)
        if not paid:
            payments = payments.filter(Review.paid == False)

        return paginate(payments \
                        .options(joinedload(cls.customers_a)) \
                        .options(joinedload(cls.doctor_a)) \
                        .options(joinedload(cls.price_list_a)) \
                        .order_by(cls.date_of_creation).all())

    ##################
    # CREATE PAYMENT #
    ##################

    @classmethod
    def edit_payment(cls, review_byid, item):
        db.query(cls).filter(cls.id == review_byid) \
            .update(item, synchronize_session=False)


# @classmethod
# def search_pdf(cls, id):
#     payments = db.query(cls)
#
#     if id:
#         payments = payments.filter(Review.id == id)
#
#     return payments \
#         .options(joinedload(cls.customers_a)) \
#         .options(joinedload(cls.doctor_a)) \
#         .options(joinedload(cls.price_list_a)) \
#         .order_by(cls.date_of_creation).all()
#
#
# @classmethod
# def get_review_unpaid(cls):
#     return db.query(cls).filter(~cls.paid) \
#         .options(joinedload(cls.customers_a)) \
#         .options(joinedload(cls.doctor_a)) \
#         .options(joinedload(cls.price_list_a)) \
#         .order_by(cls.date_of_creation).all()
#
#
# @classmethod
# def get_review_paid(cls):
#     return db.query(cls).filter(cls.paid) \
#         .options(joinedload(cls.customers_a)) \
#         .options(joinedload(cls.doctor_a)) \
#         .options(joinedload(cls.price_list_a)) \
#         .order_by(cls.date_of_creation).all()


class ReviewDocument(Base, BaseModels):
    __tablename__ = 'review_document'

    title: str
    url: str

    url = Column(String)
    title = Column(String)
    review_id = Column(Integer, ForeignKey('review.id'), nullable=False)

    review = relationship("Review", back_populates='documents')

    # __mapper_args__ = {
    #     'polymorphic_identity': 'review_document',
    # }

    # @classmethod
    # def get_review_by_id(cls, byid):
    #     return db.query(cls).filter(cls.review_id == byid).all()




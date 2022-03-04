import json

import simplejson
import datetime
import enum
from json import JSONEncoder

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy import create_engine, join, outerjoin
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


########################################################
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
        return db.query(cls).filter(cls.id == id).first()


class BaseUser(BaseModels):

    @declared_attr
    def name(self):
        return Column(String(255), nullable=False)

    # @declared_attr
    # def surname(self):
    #     return Column(String(255), nullable=False)

    # @declared_attr
    # def jmbg(self):
    #     return Column(Integer, nullable=False, unique=True)  # Unique

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
    # jmbg: int
    name: str
    # surname: str

    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.doctor)  # Enum polje

    ################################
    # GET USER BY EMAIL & PASSWORD #
    ################################

    @classmethod
    def get_user_by_email_and_password(cls, email, password):
        return db.query(cls).filter(cls.email == email, cls.password == password).first()

    #################################################
    # GET ALL USER SEARCHED BY EMAIL,NAME & SURNAME #
    #################################################

    @classmethod
    def get_all_user_paginate(cls, email, name):
        users = db.query(cls)
        if email:
            users = users.filter(cls.email == email)
        if name:
            users = users.filter(cls.name == name)
        # if surname:
        #     users = users.filter(cls.surname == surname)
        return users.all()

    #########################################
    # CHECK USER BY EMAIL , JMBG & AND ROLE #
    #########################################

    @classmethod
    def check_user_by_email(cls, email):
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def check_user_by_jmbg(cls, jmbg):
        return db.query(cls).filter(cls.jmbg == jmbg).first()

    @classmethod
    def check_user_by_role(cls, role):
        return db.query(cls).filter(cls.role == role).all()

    ##################
    # UPDATE METHODS #
    ##################
    @classmethod
    def edit_user(cls, user_id, user_data):
        db.query(cls).filter(cls.id == user_id).update(user_data, synchronize_session=False)

    @classmethod
    def get_user_by_id(cls, id):
        return db.query(cls).filter(cls.id == id).all()


class Customers(Base, BaseUser):
    __tablename__ = 'customers'

    #id: int
    #email: str
    date_of_birth = Column(DateTime)
    jmbg = Column(Integer)
    personal_medical_history = Column(Text)
    family_medical_history = Column(Text)
    company_name = Column(Text)
    company_pib = Column(Integer)
    company_address = Column(String)

    review = relationship('Review')

    #############################################################
    # JOIN VRACA CUSTOMERU POSLEDNJA 3 PREGLEDA BY EMAIL , JMBG #
    #############################################################

    @classmethod
    def get_review_by_name_paginate(cls, name):
        customers = db.query(cls).join(
            Review, Review.id == cls.id
        ).filter(Customers.name.ilike('%' + name + '%')).options(joinedload(cls.review)) \
            .order_by(cls.date_of_creation).limit(3).all()
        return customers

    ##################################
    # CHECK CUSTOMER BY EMAIL , JMBG #
    ##################################
    @classmethod
    def check_customer_by_email(cls, email):
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def check_customer_by_jmbg(cls, jmbg):
        return db.query(cls).filter(cls.jmbg == jmbg).first()

    ####################
    # GET ALL CUSTOMER #
    ####################

    @classmethod
    def get_all_customers(cls):
        customer = db.query(cls)
        return customer.all()

    ##########################
    # CHECK CUSTOMER BY JMBG #
    ##########################

    @classmethod
    def get_customer_by_jmbg(cls, jmbg):
        return db.query(cls).filter(cls.jmbg == jmbg).all()  # Stajalo je fist()umesto.all i pucalo je

    #################
    # EDIT CUSTOMER #
    #################

    @classmethod
    def edit_customer(cls, customer_id, customer_data):
        db.query(cls).filter(cls.id == customer_id).update(customer_data, synchronize_session=False)


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

    @classmethod
    def check_price_list_by_services(cls, services):
        return db.query(cls).filter(cls.services == services).first()

    ###################
    # GET ALL PRICE'S #
    ###################

    @classmethod
    def get_all_price(cls, services, medical_service):
        price_list = db.query(cls)
        if services:
            price_list = price_list.filter(cls.services == services)
        if medical_service:
            price_list = price_list.filter(cls.medical_service == medical_service)

        return price_list.all()

    ##################
    # EDIT PRICE_LIST #
    ##################

    @classmethod
    def edit_price_list(cls, price_list_id, pricelist_data):
        db.query(cls).filter(cls.id == price_list_id).update(pricelist_data, synchronize_session=False)

    @classmethod
    def delete_by_id(cls, id):
        return db.query(cls).filter(cls.id == id).all()


class Review(Base, BaseModels):
    __tablename__ = 'review'

    customers_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    price_list_id = Column(Integer, ForeignKey('price_list.id'), nullable=False)
    price_of_service = Column(Integer)
    doctor_opinion = Column(Text)



    @classmethod
    def get_review_all(cls):
        review = db.query(cls)
        # if name:
        #     users = review.filter(cls.name == name)
        # if surname:
        #     users = users.filter(cls.surname == surname)
        return review.all()

    # customers = relationship('Customers')

    ###################################
    # GET ALL REVIEW BY EMAIL OR JMBG #
    ###################################

    # @classmethod
    # def get_review_by_name_paginate(cls, name):
    #     review = db.query(cls).join(
    #         Customers, Customers.id == cls.customers_id
    #     ).filter(Customers.name.ilike('%' + name + '%')).options(joinedload(cls.customers)) \
    #       .order_by(cls.date_of_creation).limit(3).all()

    # if name:
    #     review = db.query(cls).filter(cls.name.ilike('%' + name + '%')).order_by(cls.date_of_creation).limit(3).all()
    # return review
    #  if name:
    #      review = review.filter(Customers.id == Review.customers_id)
    #  return review
    # .limit(3)

    # @classmethod
    # def join_customer_id(cls, id):
    #     result = db.query(cls)(Customers).join(Customers)
    #     for customers in result:
    #         print(customers.id)


class ReviewDocument(Base, BaseModels):
    __tablename__ = 'review_document'

    url = Column(String)
    title = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'review_document',

    }


class Payments(Base, BaseModels):
    __tablename__ = 'payments'

    review_id = Column(Integer, ForeignKey('review.id'), nullable=False)
    customers_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    price_list_id = Column(Integer, ForeignKey('price_list.id'), nullable=False)
    price_of_service = Column(Integer, nullable=False)
    paid = Column(Boolean)
    payment_made = Column(Enum(Pays), default=Pays.card)  # Enum cash, card or cash_card
    finance_id = Column(Integer, ForeignKey('review.id'), nullable=False)

    #review = relationship('Review')

    ####################
    # GET ALL PAYMENTS #
    ####################

   #@classmethod
    # def get_all_payments(cls, paid):
    #     payment = db.query(cls).join(
    #         Review, Review.id == cls.review_id
    #     ).options(joinedload(cls.review)) \
    #         .order_by(cls.date_of_creation).all()
    #     return payment
    #
    #  price_list = db.query(cls)
    # return price_list.filter(cls.paid == paid).all()

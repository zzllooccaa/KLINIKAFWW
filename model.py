import simplejson
import datetime
import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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


class BaseUser(BaseModels):

    @declared_attr
    def name(self):
        return Column(String(255), nullable=False)

    @declared_attr
    def surname(self):
        return Column(String(255), nullable=False)

    @declared_attr
    def jmbg(self):
        return Column(Integer, nullable=False, unique=True)  # Unique

    @declared_attr
    def email(self):
        return Column(String, unique=True)

    @declared_attr
    def address(self):
        return Column(String(255))

    @declared_attr
    def phone(self):
        return Column(String(20), unique=True)


@dataclass
class User(Base, BaseUser):
    __tablename__ = 'user'

    id: int
    email: str

    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.doctor)  # Enum polje

    @classmethod
    def get_user_by_email_and_password(cls, email, password):
        return db.query(cls).filter(cls.email == email, cls.password == password).first()

    @classmethod
    def get_all_user_paginate(cls, email, name, surname):
        users = db.query(cls)
        if email:
            users = users.filter(cls.email == email)
        if name:
            users = users.filter(cls.name == name)
        if surname:
            users = users.filter(cls.surname == surname)
        return users.all()

    ##################################
    # CHECK USER BY EMAIL , JMBG #
    ##################################

    @classmethod
    def check_user_by_email(cls, email):
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def check_user_by_jmbg(cls, jmbg):
        return db.query(cls).filter(cls.jmbg == jmbg).first()

    @classmethod
    def get_user_by_id(cls, id):
        return db.query(cls).filter(cls.id == id).first()

    ##################
    # UPDATE METHODS #
    ##################
    @classmethod
    def edit_user(cls, user_id, user_data):
        db.query(cls).filter(cls.id == user_id).update(user_data, synchronize_session=False)


class Customers(Base, BaseUser):
    __tablename__ = 'customers'

    id: int
    email: str
    date_of_birth = Column(DateTime)  # treba da stavis nullable=false ali vidi sa urosem
    personal_medical_history = Column(Text)
    family_medical_history = Column(Text)
    company_name = Column(Text)
    company_pib = Column(Integer)
    company_address = Column(String)

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
    def get_all_customer_paginate(cls, email, name, surname):
        customer = db.query(cls)
        if email:
            customer = customer.filter(cls.email == email)
        if name:
            customer = customer.filter(cls.name == name)
        if surname:
            customer = customer.filter(cls.surname == surname)
        return customer.all()

    @classmethod
    def get_customer_by_id(cls, id):
        return db.query(cls).filter(cls.id == id).first()

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

    @classmethod
    def check_price_list_by_medical_service(cls, medical_service):
        return db.query(cls).filter(cls.medical_service == medical_service).first()

    @classmethod
    def get_all_price(cls, service, medical_service):
        price_list = db.query(cls)
        if service:
            price_list = price_list.filter(cls.service == service)
        if medical_service:
            price_list = price_list.filter(cls.medical_service == medical_service)

        return price_list.all()


class Review(Base, BaseModels):
    __tablename__ = 'review'

    customers_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    price_list_id = Column(Integer, ForeignKey('price_list.id'), nullable=False)
    price_of_service = Column(Integer)
    doctor_opinion = Column(Text)


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

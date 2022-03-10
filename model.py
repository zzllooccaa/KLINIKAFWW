import simplejson
import datetime
from _datetime import date
import enum
from json import JSONEncoder
from fastapi_pagination import paginate

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
        return db.query(cls)\
            .filter(cls.id == id, ~User.deleted, PriceList.date_of_end == None)\
            .first()

    @classmethod
    def get_by_session_id(cls, session_id):
        return db.query(cls).filter(User.session_id == session_id, ~User.deleted).first()


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

    #reviews = relationship('Review', foreign_keys="User.reviews")

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
    def get_user_by_email_and_password(cls, email, password):
        return db.query(cls)\
            .filter(cls.email == email, cls.password == password, ~cls.deleted)\
            .first()

    #################################################
    # GET ALL USER SEARCHED BY EMAIL,NAME & SURNAME #
    #################################################

    @classmethod
    def get_all_user_paginate(cls, email, name):
        users = db.query(cls).filter(~cls.deleted)
        if email:
            users = users.filter(cls.email == email, ~User.deleted)
        if name:
            users = users.filter(cls.name == name, ~User.deleted)

        return users.all()

    #########################################
    # CHECK USER BY EMAIL , JMBG & AND ROLE #
    #########################################

    @classmethod
    def check_user_by_email(cls, email):
        return db.query(cls).filter(cls.email == email, ~User.deleted).first()

    @classmethod
    def check_user_by_jmbg(cls, jmbg):
        return db.query(cls).filter(cls.jmbg == jmbg, ~User.deleted).first()

    @classmethod
    def check_user_by_role(cls, role):
        return db.query(cls).filter(cls.role == role, ~cls.deleted).all()

    ##################
    # UPDATE METHODS #
    ##################
    @classmethod
    def edit_user(cls, user_id, user_data):
        db.query(cls).filter(cls.id == user_id, ~cls.deleted)\
            .update(user_data, synchronize_session=False)

    ##################
    # GET USER BY ID #
    ##################

    @classmethod
    def get_user_by_id(cls, id):
        return db.query(cls).filter(cls.id == id, ~cls.deleted).all()


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
    session_id: str

    date_of_birth = Column(DateTime, nullable=False)
    jmbg = Column(String)
    personal_medical_history = Column(Text)
    family_medical_history = Column(Text)
    company_name = Column(Text)
    company_pib = Column(String)
    company_address = Column(String)

    review = relationship('Review')

    #####################################################
    # JOIN VRACA CUSTOMERU POSLEDNJA 3 PREGLEDA BY NAME #
    #####################################################

    @classmethod
    def get_review_by_name_paginate(cls, name):
        customers = db.query(cls).join(
            Review, Review.id == cls.id
        ).filter(Customers.name.ilike('%' + name + '%'))\
            .options(joinedload(cls.review)) \
            .order_by(cls.date_of_creation).limit(3).all()
        return customers

    ##################################
    # CHECK CUSTOMER BY EMAIL , JMBG #
    ##################################
    @classmethod
    def check_customer_by_email(cls, email):
        return db.query(cls).filter(cls.email == email, cls.email != None).first()

    @classmethod
    def check_customer_by_jmbg(cls, jmbg):
        return db.query(cls).filter(cls.jmbg == jmbg, cls.jmbg != None).first()

    ########################
    # GET CUSTOMER BY NAME #
    ########################

    @classmethod
    def get_customers_by_name_paginate(cls, name):
        customers = db.query(cls). \
            filter(Customers.name.ilike('%' + name + '%')) \
            .order_by(cls.date_of_creation).all()
        return customers

    ####################
    # GET ALL CUSTOMER #
    ####################

    @classmethod
    def get_all_customers(cls):
        return db.query(cls).all()

    ##########################
    # CHECK CUSTOMER BY JMBG #
    ##########################

    @classmethod
    def get_customer_by_jmbg(cls, jmbg):
        return db.query(cls).filter(cls.jmbg == jmbg).all()  # Stajalo je fist()umesto.all i pucalo je

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

    @classmethod
    def check_price_list_by_services(cls, services):
        return db.query(cls)\
            .filter(cls.services == services, cls.date_of_end == None)\
            .first()

    ###################
    # GET ALL PRICE'S #
    ###################

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
        db.query(cls)\
            .filter(cls.id == price_list_id, cls.date_of_end == None)\
            .update(pricelist_data, synchronize_session=False)

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
    paid = Column(Boolean, default=False)  # True=paid , False = unpaid
    payment_made = Column(Enum(Pays), default=Pays.card)  # Enum cash, card or cash_card
    date_of_creation_payment = Column(DateTime)
    finance_id = Column(Integer, ForeignKey('user.id'))

    customers_a = relationship('Customers', viewonly=True)
    doctor_a = relationship('User', viewonly=True, foreign_keys="Review.doctor_id")
    price_list_a = relationship('PriceList', viewonly=True, foreign_keys="Review.price_list_id")

    @classmethod
    def get_review_paginate(cls):
        return paginate(db.query(cls).all())

    @classmethod
    def get_review_by_id_paginate(cls, byid):
        return paginate(db.query(cls) \
                        .filter(Review.id == byid) \
                        .options(joinedload(cls.customers_a)) \
                        .options(joinedload(cls.doctor_a)) \
                        .options(joinedload(cls.price_list_a)).all())

    @classmethod
    def get_payment_by_doctor_paginate(cls, name):
        return paginate(db.query(cls) \
                        .filter(User.name.ilike('%' + name + '%'))\
                        or filter(Review.id.ilike('%' + name + '%'))\
                        .options(joinedload(cls.customers_a)) \
                        .options(joinedload(cls.doctor_a)) \
                        .options(joinedload(cls.price_list_a)).all())

    @classmethod
    def get_review_paid(cls):
        return paginate(db.query(cls) \
                        .filter(Review.paid == True) \
                        .options(joinedload(cls.customers_a)) \
                        .options(joinedload(cls.doctor_a)) \
                        .options(joinedload(cls.price_list_a)) \
                        .order_by(cls.date_of_creation).all())


class ReviewDocument(Base, BaseModels):
    __tablename__ = 'review_document'

    url = Column(String)
    title = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'review_document',

    }

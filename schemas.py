import enum
from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from enum import Enum
from _datetime import datetime
import model
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from pydantic import EmailStr, BaseModel
from typing import List

T = TypeVar('T')


class BaseModelsSchema(BaseModel):
    id: Optional[int]
    date_of_creation: Optional[datetime]


class UserId(BaseModel):
    id: int


class UserLogin(BaseModel):
    email: str
    password: str


class RegisterUser(BaseModel):
    name: str
    role: str
    jmbg: str
    address: str
    phone: str


class AddPriceList(BaseModelsSchema):
    services: str
    medical_service: str
    price_of_service: int
    time_for_exam: int


class PaysSchema(enum.Enum):
    cash: Optional[str] = None
    card: Optional[str] = None
    cash_card: Optional[str] = None

    class Config:
        orm_mode = True


class RequestBaseModels(BaseModel):
    parameter: BaseModelsSchema = Field(...)


class BaseUserSchema(BaseModelsSchema):
    name: str
    jmbg: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        orm_mode = True


class RequestBaseUser(BaseModelsSchema):
    parameter: BaseUserSchema = Field(...)


class UserSchema(BaseUserSchema):
    password: Optional[int] = None
    role: Optional[str] = None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str]
    jmbg: Optional[str]
    phone: Optional[str]
    address: Optional[str]


class CustomerUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    jmbg: Optional[str] = None
    date_of_birth: Optional[str]
    personal_medical_history: Optional[str] = None
    family_medical_history: Optional[str] = None
    company_name: Optional[str] = None
    company_pib: Optional[str] = None
    company_address: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class CustomersSchema(BaseModel):
    date_of_birth: Optional[str] = None
    personal_medical_history: Optional[str] = None
    family_medical_history: Optional[str] = None
    company_name: Optional[str] = None
    company_pib: Optional[str] = None
    company_address: Optional[str] = None

    class Config:
        orm_mode = True


class AddCustomer(BaseModel):
    email: Optional[str] = None
    date_of_birth: Optional[str]
    personal_medical_history: Optional[str] = None
    family_medical_history: Optional[str] = None
    company_name: Optional[str] = None
    company_pib: Optional[str] = None
    company_address: Optional[str] = None
    name: str
    jmbg: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class PriceListSchema(BaseModel):
    services: Optional[str] = None
    medical_service: Optional[str] = None
    price_of_service: Optional[int] = None
    time_for_exam: Optional[int] = None

    class Config:
        orm_mode = True


class ReviewSchema(BaseModel):
    id: Optional[int] = None
    customers_id: Optional[int] = None
    doctor_id: Optional[int] = None
    price_list_id: Optional[int] = None
    price_of_service: Optional[int] = None
    doctor_opinion: Optional[str] = None

    class Config:
        orm_mode = True


class PaymentSchema(BaseModel):
    id: int
    customers_id: int
    doctor_id: int
    price_list_id: int
    price_of_service: int
    doctor_opinion: str
    paid: Optional[bool]
    payment_made: Optional[Enum]
    date_of_creation: datetime
    finance_id: Optional[int]
    doctor_a: BaseUserSchema
    customer_a: CustomersSchema
    price_list_a: PriceListSchema

    class Config:
        orm_mode = True


class ReviewDocumentSchema(BaseModel):
    id: Optional[int] = None
    url: Optional[str] = None
    title: Optional[str] = None
    review_id: Optional[int] = None

    class Config:
        orm_mode = True


class NewReview(BaseModel):
    doctor_opinion: Optional[str] = None
    price_of_service: Optional[int] = None
    customers_id: int
    price_list_id: int


class NewPayments(BaseModel):
    paid: bool
    payment_made: str

    class Config:
        orm_mode = True


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]


class PagePerPage(BaseModel):
    email: Optional[str]
    name: Optional[str]
    surname: Optional[str]


class SessionData(UserId):
    username: str
    role: Enum


class UserRead(BaseUserSchema):
    id: int


class ForgotPassword(BaseModel):
    email: str


class RecoverPassword(BaseModel):
    password: str


###################
# RESPONSE SCHEMA #
###################
class ReviewDocumentResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = model.ReviewDocument


class CustomersResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = model.Customers


class ReviewResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = model.Review

    documents = fields.Nested(ReviewDocumentResponseSchema, many=True)
    customers_a = fields.Nested(CustomersResponseSchema, many=False)


class ReviewCustomersResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = model.Customers

    review = fields.Nested(ReviewResponseSchema, many=True)


class ResponseReviewSchema(BaseModel):
    id: Optional[int] = None
    customers_id: Optional[int] = None
    doctor_id: Optional[int] = None
    price_list_id: Optional[int] = None
    price_of_service: Optional[int] = None
    doctor_opinion: Optional[str] = None
    paid: Optional[bool]
    payment_made: Optional[str]


class EmailSchema(BaseModel):
    email: List[EmailStr]




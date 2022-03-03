from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from enum import Enum
from _datetime import datetime

T = TypeVar('T')


class UserId(BaseModel):
    id: int


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    #jmbg: Optional[int] = None
    role: Optional[str] = None


class CustomerUpdate(BaseModel):
    email: Optional[str] = None
    date_of_birth: Optional[str] = None
    personal_medical_history: Optional[str] = None
    family_medical_history: Optional[str] = None
    company_name: Optional[str] = None
    company_pib: Optional[int] = None
    company_address: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    jmbg: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[int] = None


class RegisterUser(UserLogin):
    name: str
    #surname: str
    role: str


class AddPriceList(UserId):
    services: str
    medical_service: str
    price_of_service: int
    time_for_exam: int


class RoleSchema(Enum):
    admin: Optional[str] = None
    doctor: Optional[str] = None
    finance: Optional[str] = None

    class Config:
        orm_mode = True


class PaysSchema(Enum):
    cash: Optional[str] = None
    card: Optional[str] = None
    cash_card: Optional[str] = None

    class Config:
        orm_mode = True


class BaseModelsSchema(BaseModel):
    id: Optional[int]
    date_of_creation: Optional[int] = None


class RequestBaseModels(BaseModel):
    parameter: BaseModelsSchema = Field(...)


class BaseUserSchema(BaseModelsSchema):
    name: Optional[str] = None
    surname: Optional[str] = None
    jmbg: Optional[int] = None
    email: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[int] = None

    class Config:
        orm_mode = True


class RequestBaseUser(BaseModelsSchema):
    parameter: BaseUserSchema = Field(...)


class UserSchema(BaseUserSchema):
    password: Optional[int] = None
    role: Optional[str] = None

    class Config:
        orm_mode = True


class CustomersSchema(BaseUserSchema):
    date_of_birth: Optional[int] = None
    personal_medical_history: Optional[str] = None
    family_medical_history: Optional[str] = None
    company_name: Optional[str] = None
    company_pib: Optional[int] = None
    company_address: Optional[str] = None

    class Config:
        orm_mode = True


class AddCustomer(UserId):
    email: Optional[str] = None
    date_of_birth: str
    personal_medical_history: Optional[str] = None
    family_medical_history: Optional[str] = None
    company_name: Optional[str] = None
    company_pib: Optional[int] = None
    company_address: Optional[str] = None
    name: str
    jmbg: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[int] = None


class PriceListSchema(BaseModel):
    services: Optional[str] = None
    medical_service: Optional[str] = None
    price_of_service: Optional[int] = None
    time_for_exam: Optional[int] = None
    date_of_end: datetime = None

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


class ReviewDocumentSchema(BaseModel):
    id: Optional[int] = None
    url: Optional[str] = None
    title: Optional[str] = None

    class Config:
        orm_mode = True


class NewReview(BaseModel):
    #id: str
    doctor_opinion: Optional[str] = None
    price_of_service: Optional[int] = None
    customers_id: int
    price_list_id: int


class PaymentsSchema(BaseModel):
    id: Optional[int] = None
    review_id: Optional[int] = None
    customers_id: Optional[int] = None
    user_id: Optional[int] = None
    price_list_id: Optional[int] = None
    price_of_service: Optional[int] = None
    paid: Optional[int] = None
    payment_made: Optional[str] = None
    finance_id: Optional[int] = None

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

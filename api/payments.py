from fastapi import APIRouter, Depends, HTTPException

import schemas
from model import db, Review, User
from examples import payments_example

from utils import auth_user, get_user_from_header
from fpdf import FPDF

import errors
import datetime

from fastapi_pagination import Page

payments_router = APIRouter()


@payments_router.patch("/create/{review_id}")
def create_payment(review_id, item: schemas.NewPayments = payments_example,
                   current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['finance'])
    review_check = Review.get_by_id(id=review_id)
    if not review_check:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)

    try:
        payments = Review(
            finance_id=current_user.id,
            paid=item.paid,
            payment_made=item.payment_made,
            date_of_creation_payment=datetime.datetime.now()
        )
        db.add(payments)
        db.commit()
        return payments
    except Exception as e:
        db.rollback()
        print(e)
        return {'ERROR': 'ERR_DUPLICATED_ENTRY'}


@payments_router.get("/get_all_payments/", response_model=Page)
# @payments_router.get("/get_all_review/limit-offset", response_model=LimitOffsetPage)
def get_all_payments(item: str = None, byid: int = None, paid: bool = None,
                     current_user: User = Depends(get_user_from_header)):  # schemas.PaymentSearch,
    auth_user(user=current_user, roles=['finance'])
    review_check = Review.search_payments(name=item, id=byid, paid=paid)
    return review_check


@payments_router.get("/create_pdf")
def get_create_pdf(byid: int = None, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['finance'])

    doc = Review.get_by_id(id=byid)
    if not doc:
        return errors.ERR_ID_NOT_EXIST

    class PDF(FPDF):
        def header(self):
            self.set_font('helvetica', 'B', 20)

            self.cell(30, 10, 'Invoice', border=False)
            self.set_font('helvetica', 'B', 10)
            self.cell(130, 10, 'Klinika d.o.o', border=False, ln=True)
            self.set_font('helvetica', 'B', 8)
            self.cell(30, 10, 'Komercijalna Banka: 121-12312312313-213123', border=False, ln=True)
            self.cell(130, 10, 'Address Milutina Milankovica 195', border=False, ln=True)
            self.cell(130, 10, '11000 Belgrade', border=False, ln=True)
            self.cell(130, 10, 'Phone 011/3223-2311', border=False, ln=True)

            self.ln(20)

    pdf = PDF('L', 'mm', 'A4')

    pdf.add_page()

    pdf.set_font('helvetica', '', 10)

    pdf.cell(30, 10, 'Date:')
    pdf.cell(10, 10, str(datetime.date.today()), ln=True)

    pdf.line(30, 30, 180, 30)
    pdf.set_font('helvetica', 'BU', 12)
    pdf.cell(130, 10, 'Customer')
    pdf.cell(35, 10, 'Company ', ln=True)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(30, 10, 'name : ')
    pdf.set_font('helvetica', '', 8)
    pdf.cell(100, 10, doc.customers_a.name)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(35, 10, 'company-name : ')
    pdf.set_font('helvetica', '', 8)
    pdf.cell(195, 10, doc.customers_a.company_name, ln=True)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(30, 10, 'Address:', )
    pdf.set_font('helvetica', '', 8)
    pdf.cell(100, 10, doc.customers_a.address)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(35, 10, 'Address:', )
    pdf.set_font('helvetica', '', 8)
    pdf.cell(195, 10, doc.customers_a.company_address, ln=True)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(30, 10, 'Phone:', )
    pdf.set_font('helvetica', '', 8)
    pdf.cell(100, 10, doc.customers_a.phone)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(35, 10, 'company PIB:', )
    pdf.set_font('helvetica', '', 8)
    pdf.cell(195, 10, str(doc.customers_a.company_pib), ln=True)
    pdf.line(10, 30, 200, 30)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(45, 10, 'Description:', ln=True, border=True)
    pdf.set_font('helvetica', 'I', 8)
    pdf.cell(190, 10, doc.price_list_a.services, border=True, ln=True)
    pdf.cell(190, 10, doc.price_list_a.medical_service, border=True, ln=True)
    pdf.set_font('helvetica', 'B', 8)
    pdf.cell(15, 10, 'price', border=True)
    pdf.cell(20, 10, str(doc.price_list_a.price_of_service), border=True)
    pdf.cell(15, 10, 'RSD', border=True, ln=True)
    pdf.set_font('helvetica', 'B', 6)
    pdf.cell(35, 10, 'date of exam')
    pdf.cell(15, 10, str(doc.date_of_creation), ln=True)
    pdf.image(name='/home/fww1/Downloads/klinika.jpeg', x=235, y=0, w=40, h=40, type='JPEG', link='pdf.add_link()')

    pdf.output('invoice.pdf')

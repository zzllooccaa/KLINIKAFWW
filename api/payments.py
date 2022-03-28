from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from fastapi.responses import FileResponse

import schemas
from model import db, Review, User
from config import path_doc, path_req

from utils import auth_user, get_user_from_header
from fpdf import FPDF
import errors
import datetime


payments_router = APIRouter()


@payments_router.patch("/{review_id}")
def create_payment(review_id, item: schemas.NewPayments,
                   current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['finance'])
    review_check = Review.get_by_id(id=review_id)
    if not review_check:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)

    payment_d = item.dict(exclude_none=True)
    Review.edit_payment(review_byid=review_id, item=payment_d)
    review_check.date_of_creation_payment = datetime.datetime.now()
    review_check.finance_id = current_user.id
    db.add(review_check)
    db.commit()
    db.refresh(review_check)
    return review_check


@payments_router.get("/get_all_payments/", response_model=Page)
def get_all_payments(item: str = None, by_id: int = None, paid: bool = None,
                     current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['finance'])
    review_checks = Review.search_payments(name=item, id=by_id, paid=paid)
    return review_checks


@payments_router.get("/download/{create_by_id}")
def get_create_pdf(by_id: int = None, current_user: User = Depends(get_user_from_header)):
    auth_user(user=current_user, roles=['finance'])

    doc = Review.get_by_id(id=by_id)
    if not doc:
        return HTTPException(status_code=400, detail=errors.ERR_ID_NOT_EXIST)

    class PDF(FPDF):
        def header(self):
            self.set_font('helvetica', 'B', 20)

            self.cell(30, 10, 'Invoice', border=False)
            self.set_font('helvetica', 'B', 10)
            self.cell(130, 10, 'Klinika d.o.o', border=False, ln=True)
            self.set_font('helvetica', 'B', 8)
            self.cell(30, 10, 'Komercijalna Banka: 121-12312312313-213123', border=False, ln=True)
            self.cell(130, 6, 'Address Milutina Milankovica 195', border=False, ln=True)
            self.cell(130, 6, 'PIB 2312141124', border=False, ln=True)
            self.cell(130, 6, 'maticni broj 231000223', border=False, ln=True)
            self.cell(130, 6, '11000 Belgrade', border=False, ln=True)
            self.cell(130, 6, 'Phone 011/3223-2311', border=False, ln=True)

            self.ln(20)

    pdf = PDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.line(10, 60, 60, 60)
    pdf.set_font('helvetica', '', 8)
    pdf.cell(10, 2, 'Date:')
    pdf.cell(10, 2, str(datetime.date.today()), ln=True)

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(130, 20, 'Customer')
    pdf.cell(35, 20, 'Company ', ln=True)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(30, 5, 'name : ')
    pdf.set_font('helvetica', '', 8)
    pdf.cell(100, 5, doc.customers_a.name)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(35, 5, 'company-name : ')
    pdf.set_font('helvetica', '', 8)
    pdf.cell(195, 5, doc.customers_a.company_name, ln=True)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(30, 5, 'Address:', )
    pdf.set_font('helvetica', '', 8)
    pdf.cell(100, 5, doc.customers_a.address)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(35, 5, 'Address:', )
    pdf.set_font('helvetica', '', 8)
    pdf.cell(195, 5, doc.customers_a.company_address, ln=True)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(30, 5, 'Phone:', )
    pdf.set_font('helvetica', '', 8)
    pdf.cell(100, 5, doc.customers_a.phone)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(35, 5, 'company PIB:', )
    pdf.set_font('helvetica', '', 8)
    pdf.cell(195, 5, str(doc.customers_a.company_pib), ln=True)
    pdf.line(10, 30, 200, 30)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(45, 5, 'Description:', ln=True, border=True)
    pdf.set_font('helvetica', 'I', 8)
    pdf.cell(190, 5, doc.price_list_a.services, border=True, ln=True)
    pdf.cell(190, 5, doc.price_list_a.medical_service, border=True, ln=True)
    pdf.set_font('helvetica', 'B', 8)
    pdf.cell(15, 5, 'price', border=True)
    pdf.cell(20, 5, str(doc.price_list_a.price_of_service), border=True)
    pdf.cell(15, 5, 'RSD', border=True, ln=True)
    pdf.set_font('helvetica', 'B', 6)
    pdf.cell(35, 5, 'date of service')
    pdf.cell(15, 5, str(doc.date_of_creation), ln=True)
    pdf.image(name=path_req + "/" + 'klinika.jpeg', x=170, y=0, w=40, h=30, type='JPEG', link='pdf.add_link()')
    pdf.set_font('helvetica', 'B', 6)
    pdf.cell(0, 10, 'email: klinika@finance.com')

    pdf.output(path_doc + f'/invoice.pdf')
    name_file = 'invoice.pdf'
    print(name_file)

    return FileResponse(path=path_doc + "/" + 'invoice.pdf', media_type='application/octet-stream', filename=name_file)

from fastapi import APIRouter, Depends
from model import Review, Role

import errors
from sess.sess_fronted import cookie

from sess.sess_verifier import SessionData, verifier

review_router = APIRouter()


@review_router.post("/create", dependencies=[Depends(cookie)])
def create_review(session_data: SessionData = Depends(verifier)):
    ##############################################################
    # CHECK user role. If user is not doctor, then return error. #
    ##############################################################
    if session_data.role.name != Role.doctor.name:
        return errors.ERR_USER_NOT_GRANTED
    return True


@review_router.get("/get_review_by_email_and_jmbg")
def get_all_review(jmbg: int = None, email: str = None):
    review = Review.get_all_review_paginate(jmbg=jmbg, email=email)
    return review

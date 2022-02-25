from fastapi import APIRouter, HTTPException, Path, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import RequestBaseUser, ReviewDocumentSchema, RoleSchema, BaseUserSchema, \
    BaseModelsSchema, PaysSchema, \
    PaymentsSchema, PriceListSchema, CustomersSchema, UserSchema, Response
import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create-base-user')
async def create_base_user(request: RequestBaseUser, db: Session = Depends(get_db)):
    crud.create_base_user(db, request.parameter)
    return Response(code=200, status="ok", message="Baseuser created successfully").dict(exclude_none=True)


@router.get("/")
async def get(db:Session=Depends(get_db)):
    _user = crud.get_user(db,0,100)
    return Response(code=200, status="ok", message="Seccess fetch all data", result=_user).dict(exclude_none=True)

@router.get("/{id}")
async def get_by_id(id:int,db:Session = Depends(get_db)):
    _user = crud.get_user_by_id(db,id)
    return Response(code=200, status="ok", message="Success", result=_user).dict(exclude_none=True)

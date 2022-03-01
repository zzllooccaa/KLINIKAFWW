from fastapi import FastAPI

from api.user import user_router
from api.customer import customer_router
from api.pricelist import price_list_router
from api.review import review_router
from api.payments import payments_router


app = FastAPI()

app.include_router(
    user_router,
    prefix="/user",
    tags=["user"],
)

'#Ubaci customer router'
app.include_router(
     customer_router,
     prefix="/customer",
     tags=["customer"],
 )

app.include_router(
     price_list_router,
     prefix="/price-list",
     tags=["price-list"],
 )

app.include_router(
     review_router,
     prefix="/review",
     tags=["review"],
 )

app.include_router(
     payments_router,
     prefix="/payments",
     tags=["payments"],
 )


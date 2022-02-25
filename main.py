from fastapi import FastAPI
from api.user import user_router
from api.customer import customer_router
from api.pricelist import price_list_router
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

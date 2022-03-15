from fastapi import FastAPI
import uvicorn
from api.user import user_router
from api.customer import customer_router
from api.pricelist import price_list_router
from api.review import review_router
from api.payments import payments_router
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    user_router,
    prefix="/user",
    tags=["user"],
)

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

add_pagination(app)

add_pagination(app)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

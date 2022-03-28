from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

import logging
import uvicorn

from api.user import user_router
from api.customer import customer_router
from api.pricelist import price_list_router
from api.review import review_router
from api.payments import payments_router
from api.forgot_password import forgot_password_router
from api.logger import logger
from api.logger import init_logging

init_logging()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

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

app.include_router(
    forgot_password_router,
    prefix="/forgot_password",
    tags=["forgot_password"],
)

add_pagination(app)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    import time
    logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
    start_time = time.time()

    # Call function
    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(process_time)

    logging.getLogger("fastapi").debug("Start")
    # logger.bind(payload=(request.url)).info("URL")
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

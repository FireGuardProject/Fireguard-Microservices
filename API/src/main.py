from fastapi import FastAPI
from fastapi.routing import APIRoute
from api import api_router

# Create an instance of the FastAPI class
app = FastAPI()


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(api_router, prefix="/api")

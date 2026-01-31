from fastapi import FastAPI
from view import router as view_router
from router import router as pacient_router

app = FastAPI()
app.include_router(view_router)
app.include_router(pacient_router)



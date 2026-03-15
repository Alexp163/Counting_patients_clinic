from view import router as view_router
from router import router as pacient_router
from app import app
from admin import *  

app.include_router(view_router)
app.include_router(pacient_router)



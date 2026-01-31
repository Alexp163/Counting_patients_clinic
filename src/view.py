from fastapi import APIRouter, Depends, Request, status, Form
from datetime import datetime

from database import get_async_session
from templates import render_template

router = APIRouter(tags=["index"])


@router.get("/index_2")
async def index(request: Request):
    return render_template("index.html", request=request)

@router.get("/")
async def index_login(request: Request):
    return render_template("index_login.html", request=request)


@router.get("/pacients")
async def pacients(request: Request):
    return render_template("pacients.html", request=request)


@router.get("/report")
async def report(request: Request):
    return render_template("report.html", request=request)


@router.post("/")
async def index_post(request: Request, fio: str = Form(), date_birth: datetime = Form(), password: str = Form()):
    print(fio, date_birth, password)
    return render_template("index.html", request=request)



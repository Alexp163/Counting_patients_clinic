from fastapi import APIRouter, Depends, Request, status, Form
from sqlalchemy import insert, select
from datetime import datetime

from database import get_async_session
from templates import render_template
from models import Pacient, LoginPassword

router = APIRouter(tags=["index"])


@router.get("/")
async def index(request: Request):
    return render_template("login_password.html", request=request)


@router.post("/login_password")
async def login_password(request: Request, session=Depends(get_async_session),
                         login: str | None  = Form(default=None), 
                         password:str | None = Form(default=None)):
    print(login, password)
    statement = select(LoginPassword).where((LoginPassword.login == login) &
                                            (LoginPassword.password == password))
    result = await session.scalar(statement)
    if result == None:
        return render_template("login_password.html", request=request, message="Неверный логин или пароль")
    print(result)
    print("Проверка пройдена2")
    return render_template("list_pacients.html", request=request)


@router.get("/pacients") # регистрация пациента
async def pacients(request: Request):
    return render_template("pacients.html", request=request)


@router.get("/report")  # отчет кто состоит на сегодняшний день
async def report(request: Request, session=Depends(get_async_session)):
    statement = select(Pacient)
    return render_template("report.html", request=request)

@router.get("/list_pacients") # вывести пациентов за указанный период
async def list_pacients(request: Request):
    return render_template("list_pacients.html", request=request)


@router.post("/list_pacients") # вывести пациентов за указанный период
async def list_pacients_post(request: Request, session=Depends(get_async_session), 
                             date_start: datetime = Form(default=None), 
                             date_end: datetime = Form(default=None), 
                             location_clinics: list[str] = Form(default=None)):    
    if date_start is None or date_end is None or location_clinics is None:
        return render_template("list_pacients.html", request=request, message="Заполните все поля")
    print(date_start, date_start, location_clinics)
    statement = select(Pacient).where(
        ((Pacient.date_end != None) & (Pacient.date_end >= date_start) & 
         (Pacient.date_start <= date_end)) | ((Pacient.date_end == None) & 
                                              (Pacient.date_start <= date_end))
    ).where(Pacient.location_clinic.in_(location_clinics))
    result = list(await session.scalars(statement))
    for pacient in result:
        if pacient.date_end != None:
            pacient.days = (pacient.date_end - pacient.date_start).days # поставить "-1"  если считаем к/дни точно
        else:
            pacient.days = (datetime.now() - pacient.date_start).days
        print()
    dictionary = {}
    for value in result:
        dictionary[value.location_clinic] = []
    for value in result:
        dictionary[value.location_clinic].append(value)
    for clinic in dictionary:
        for pacient in dictionary[clinic]:
            print("-", pacient.fio, pacient.date_start.date())
    if dictionary == {}:
        description = "По введенным датам пациенты в указанных филиалах не найдены, попробуйте задать другие параметры ввода"
    else:
        description = "Пациенты на стационарном лечении в клиниках по отделениям: "
    return render_template("list_pacients.html", request=request, dictionary=dictionary, description=description)


@router.get("/enter_pacients")  # вывести списком пациентов на настоящий день
async def enter_pacients(request: Request, session=Depends(get_async_session)):
    statement = select(Pacient).where(Pacient.date_end == None)
    result = list(await session.scalars(statement))
    dictionary = {}
    for value in result:
        dictionary[value.location_clinic] = []
    for value in result:
        dictionary[value.location_clinic].append(value)
    for clinic in dictionary:
        for pacient in dictionary[clinic]:
            print("-", pacient.fio, pacient.date_start.date())
    return render_template("enter_pacients.html", request=request, dictionary=dictionary)


@router.post("/pacients_accept") # зарегистрировать пациента
async def pacients_accept(request: Request, fio: str | None = Form(default=None), date_birth: datetime | None = Form(default=None), 
                          date_start: datetime | None = Form(default=None), location_clinic: str = Form(),
                          session=Depends(get_async_session)):
    if date_birth is None or date_start is None or fio is None:
        return render_template("pacients.html", request=request, message="Заполните все поля")
    statement = insert(Pacient).values(
        fio=fio,
        date_birth=date_birth,
        date_start=date_start,
        location_clinic=location_clinic,
        status=True,
    )
    await session.execute(statement)
    await session.commit()
    return render_template("pacients.html", request=request, message=f"{fio} зарегистрирован")



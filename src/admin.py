from sqladmin import Admin
from sqladmin import ModelView
from wtforms import SelectField

from app import app
from database import engine
from models import Pacient, LoginPassword
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend





class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """Функция, проверяющая данные в форме авторизации"""

        form = await request.form()
        username, password = form["username"], form["password"]
        if username == "AlexAdmin" and password == "9502039Popov+++":
            request.session.update({"token": "1234"})
            return True
        else:
            return False

    async def logout(self, request: Request) -> bool:
        """Функция, проверяющая был ли авторизован пользователь"""
        request.session.clear()

    async def authenticate(self, request: Request) -> bool:
        """Функция, проверяющая был ли авторизован пользователь"""

        token = request.session.get("token")

        if token is not None and token == "1234":
            return True
        else:
            return False

sqladmin = AdminAuth(secret_key="09485u42[w5lkjkjk")
admin = Admin(app, engine, authentication_backend=sqladmin)


class PacientModelView(ModelView, model=Pacient):
    column_list = [Pacient.fio, Pacient.date_birth, Pacient.date_start, Pacient.date_end, 
                   Pacient.location_clinic]
    form_overrides = {
        "location_clinic": SelectField
    }

    form_args ={
        "location_clinic": {
            "choices":[
                ("МЦ Искровская","МЦ Искровская"),
                ("РЦ Искровская","РЦ Искровская"),
                ("РЦ Некрасовская","РЦ Некрасовская"),
                ("МЦ Владимирская","МЦ Владимирская"),
                ("Доверие","Доверие")
            ]
        }
    }


class LoginPasswordModelView(ModelView, model=LoginPassword):
    column_list = [LoginPassword.login, LoginPassword.password]


admin.add_view(PacientModelView)
admin.add_view(LoginPasswordModelView)


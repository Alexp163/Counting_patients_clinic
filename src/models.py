from database import Base 
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import false, true



class Pacient(Base):
    __tablename__ = "pacient"
    id: Mapped[int] = mapped_column(primary_key=True)
    fio: Mapped[str] = mapped_column()
    date_birth: Mapped[datetime] = mapped_column()
    status: Mapped[bool] = mapped_column(server_default=true())
    location_clinic: Mapped[str] = mapped_column()
    date_start: Mapped[datetime] = mapped_column(server_default=func.now())
    date_end: Mapped[datetime | None] = mapped_column(server_default=None)


    def __repr__(self):
        return f"{self.id} {self.fio} {self.status} {self.location_clinic} "


class LoginPassword(Base):
    __tablename__ = "login_password"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"{self.login} {self.password}"
    

from database import Base 
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import false



class Pacient(Base):
    __tablename__ = "pacient"
    id: Mapped[int] = mapped_column(primary_key=True)
    fio: Mapped[str] = mapped_column()
    date_birth: Mapped[datetime] = mapped_column()
    status: Mapped[bool] = mapped_column(server_default=false())
    location_clinic: Mapped[str] = mapped_column()
    date_start: Mapped[datetime] = mapped_column(server_default=func.now())
    date_end: Mapped[datetime | None] = mapped_column(server_default=None)


    def __repr__(self):
        return f"{self.id} {self.fio} {self.date_birth} {self.status} {self.location_clinic} {self.date_start} {self.date_end}"



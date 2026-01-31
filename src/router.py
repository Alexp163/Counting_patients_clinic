from fastapi import APIRouter, status, Depends
from schemas import PacientCreateSchema, PacientReadSchema, PacientUpdateSchema
from sqlalchemy import select, insert, delete, update 

from database import get_async_session
from models import Pacient 


router = APIRouter(tags=["pacients"], prefix="/pacients")

@router.post("/", status_code=status.HTTP_201_CREATED) # 1) Создание пациента
async def create_pacient(pacient: PacientCreateSchema, session=Depends(get_async_session)) -> PacientReadSchema:
    statement = insert(Pacient).values(
        fio=pacient.fio,
        date_birth=pacient.date_birth,
        status=pacient.status,
        date_start=pacient.date_start,
        date_end=pacient.date_end,
    ).returning(Pacient)
    result = await session.scalar(statement)
    await session.commit()
    return result 


@router.get("/", status_code=status.HTTP_202_ACCEPTED)  # 2) Получает данные от всех пациентах 
async def get_pacients(session=Depends(get_async_session)) -> list[PacientReadSchema]:
    statement = select(Pacient)
    result = await session.scalars(statement)
    return list(result)


@router.get("/{pacient_id}", status_code=status.HTTP_202_ACCEPTED)  #  3) Получение данных о пользователе по id 
async def get_pacient_by_id(pacient_id: int, session=Depends(get_async_session)) -> PacientReadSchema:
    statement = select(Pacient).where(Pacient.id == pacient_id)
    result = await session.scalar(statement)
    return result 


@router.delete("/{pacient_id}", status_code=status.HTTP_204_NO_CONTENT)  # 4) Удаление пациента по id 
async def delete_pacient_by_id(pacient_id: int, session=Depends(get_async_session)) -> None:
    statement = delete(Pacient).where(Pacient.id == pacient_id)
    await session.execute(statement)
    await session.commit()


@router.put("/{pacient_id}", status_code=status.HTTP_200_OK)  # 5) Обновление данных пациента по id 
async def upgrade_pacient_by_id(pacient_id: int, pacient: PacientUpdateSchema, 
                                session=Depends(get_async_session)) -> PacientReadSchema:
    statement = update(Pacient).where(Pacient.id == pacient_id).values(
        fio=pacient.fio,
        date_birth=pacient.date_birth,
        status=pacient.status,
        date_start=pacient.date_start,
        date_end=pacient.date_end,
    ).returning(Pacient)
    result = await session.scalar(statement)
    await session.commit()
    return result 


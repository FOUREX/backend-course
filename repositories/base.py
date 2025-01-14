from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, **values):
        stmt = insert(self.model).values(**values).returning(self.model)

        result = await self.session.execute(stmt)

        return result.scalars().one()

    async def edit(self, values: dict, **filter_by) -> None:
        stmt = update(self.model).filter_by(**filter_by).values(**values)
        return None

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        return None


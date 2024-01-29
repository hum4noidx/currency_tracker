from sqlalchemy import select, update

from app.models import Cource
from app.repo.repo import SQLAlchemyRepo


class CoursesRepo(SQLAlchemyRepo):
    async def get_courses(
        self, trade_pair: str = None, exchange: str = None
    ) -> list[Cource]:
        query = select(Cource)
        if trade_pair:
            query = query.where(Cource.trade_pair == trade_pair)
        if exchange:
            query = query.where(Cource.exchanger.has(name=exchange))
        result = await self.session.execute(query)
        return result.scalars().all() if result else []

    async def update_courses(self, courses: list[Cource]):
        for cource in courses:
            await self.session.execute(
                update(Cource)
                .where(Cource.trade_pair == cource.trade_pair)
                .where(Cource.exchange_id == cource.exchange_id)
                .values(value=cource.value)
            )

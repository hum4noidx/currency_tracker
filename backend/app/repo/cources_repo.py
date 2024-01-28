from sqlalchemy import select

from app.models import Cource
from app.repo.repo import SQLAlchemyRepo


class CourcesRepo(SQLAlchemyRepo):
    async def get_cources(self, trade_pair: str = None, exchange: str = None) -> list[Cource]:
        query = select(
            Cource
        )
        if trade_pair:
            query = query.where(Cource.trade_pair == trade_pair)
        if exchange:
            query = query.where(Cource.exchanger.has(name=exchange))
        result = await self.session.execute(query)
        return result.scalars().all() if result else []

import contextlib
import logging
from typing import List

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session_maker
from app.models import Cource
from app.repo.courses_repo import CoursesRepo

logger = logging.getLogger(__name__)


class BinanceExchanger:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.courses_repo = CoursesRepo(self.session)

    async def _create_db_session(self):
        async with async_session_maker() as session:
            self.session = yield session
            await session.close()

    @contextlib.asynccontextmanager
    async def _create_aiohttp_client(self):
        async with aiohttp.ClientSession() as session:
            yield session

    async def get_courses(self, trade_pair: List[str]) -> dict | None:
        async with self._create_aiohttp_client() as session:
            symbols_string = ",".join(f'"{symbol}"' for symbol in trade_pair)
            params = {"symbols": f"[{symbols_string}]"}
            async with session.get(
                "https://api.binance.com/api/v3/ticker/price",
                params=params,
            ) as response:
                logger.debug(f"Got response from binance: {response.status}")
                try:
                    response.raise_for_status()
                    logger.debug("Response is ok")
                except aiohttp.ClientResponseError as e:
                    logger.error(f"Error while getting courses from binance: {e}")
                    return None
                logger.debug("Returning response as json")
                return await response.json()

    async def get_and_save_courses(self, trade_pair: List[str]):
        logger.debug("Using binance exchanger to get courses")
        courses = await self.get_courses(trade_pair)
        if not courses:
            logger.warning("No updates received from binance")
            return
        logger.debug(f"Got {len(courses)} courses from binance")
        await self.courses_repo.update_courses(
            [
                Cource(
                    trade_pair=cource["symbol"],
                    value=float(cource["price"]),
                    exchange_id=1,  # for demonstration purposes
                )
                for cource in courses
            ]
        )
        await self.session.commit()
        logger.info(f"Saved {len(courses)} courses from binance")

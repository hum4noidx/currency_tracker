import logging

from app.db import async_session_maker
from app.services.binance_exchanger import BinanceExchanger

logger = logging.getLogger(__name__)


async def update_courses():
    logger.debug("Starting courses update from binance")
    async with async_session_maker() as session:
        logger.debug("Created db session")
        exchanger = BinanceExchanger(session)
        await exchanger.get_and_save_courses(
            ["BTCRUB", "BTCUSDT", "ETHRUB", "ETHUSDT", "USDTRUB"]
        )

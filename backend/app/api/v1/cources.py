import logging

from fastapi import APIRouter

from app.deps.db import CurrentAsyncSession
from app.repo.cources_repo import CourcesRepo

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/cources",
    tags=["cources"],
)


@router.get("/")
async def get_cources(
    session: CurrentAsyncSession,
    trade_pair: str = None,
    exchange: str = None,
):
    cources_repo: CourcesRepo = CourcesRepo(session)
    cources = await cources_repo.get_cources(trade_pair, exchange)
    return cources

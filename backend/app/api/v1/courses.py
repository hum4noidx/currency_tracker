import logging

from fastapi import APIRouter

from app.deps.db import CurrentAsyncSession
from app.repo.courses_repo import CoursesRepo

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
)


@router.get("/")
async def get_courses(
    session: CurrentAsyncSession,
    trade_pair: str = None,
    exchange: str = None,
):
    courses_repo: CoursesRepo = CoursesRepo(session)
    courses = await courses_repo.get_courses(trade_pair, exchange)
    return courses

from typing import Optional, Union

from sqlalchemy import and_, or_
from app.common.crud import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID
from sqlalchemy.orm import joinedload

from app.match_history.model import CurrentSeasonSummaries, MatchHistories
from app.match_history.schema import (
    ICurrentSeasonSummariesCreate,
    ICurrentSeasonSummariesUpdate,
    IMatchHistoriesCreate,
    IMatchHistoriesUpdate,
)
from app.common.model import Items


class CRUDMatchHistories(
    CRUDBase[MatchHistories, IMatchHistoriesCreate, IMatchHistoriesUpdate]
):
    def get_user_match_histories(self, *, summoner_name: str, db_session=None):
        db_session = db_session
        query = (
            select(MatchHistories).where(MatchHistories.summoner_name == summoner_name)
            # .options(joinedload(MatchHistories.item_0))
        )
        response = db_session.execute(query)
        return response.scalars().all()


match_history_crud = CRUDMatchHistories(MatchHistories)


class CRUDCurrentSeasonSummaries(
    CRUDBase[
        CurrentSeasonSummaries,
        ICurrentSeasonSummariesCreate,
        ICurrentSeasonSummariesUpdate,
    ]
):
    def get_by_puu_id_queue(self, *, puu_id: str, queue_id: int, db_session=None):
        db_session = db_session
        query = select(CurrentSeasonSummaries).where(
            and_(
                CurrentSeasonSummaries.puu_id == puu_id,
                CurrentSeasonSummaries.queue_id == queue_id,
            )
        )
        response = db_session.execute(query)
        return response.scalar_one_or_none()

    def remove_summoner_summaries(self, *, puu_id: str, db_session=None):
        db_session = db_session

        response = db_session.execute(
            select(CurrentSeasonSummaries).where(
                CurrentSeasonSummaries.puu_id == puu_id
            )
        )
        obj = response.scalars()

        db_session.delete(obj)
        db_session.commit()
        return obj


current_season_summaries_crud = CRUDCurrentSeasonSummaries(CurrentSeasonSummaries)

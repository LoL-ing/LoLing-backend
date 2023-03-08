from typing import Optional, Union
from app.common.crud import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.match_history.model import MatchHistories
from app.match_history.schema import IMatchHistoriesCreate, IMatchHistoriesUpdate


class CRUDMatchHistories(
    CRUDBase[MatchHistories, IMatchHistoriesCreate, IMatchHistoriesUpdate]
):
    pass


match_history_crud = CRUDMatchHistories(MatchHistories)

from app.match_history.model import (
    CurrentSeasonSummaries,
    CurrentSeasonSummariesBase,
    MatchHistoriesBase,
)
from uuid import UUID

from app.common.utils import optional


class IMatchHistoriesCreate(MatchHistoriesBase):
    pass


class IMatchHistoriesRead(MatchHistoriesBase):
    id: UUID


# All these fields are optional
@optional
class IMatchHistoriesUpdate(CurrentSeasonSummaries):
    pass


class ICurrentSeasonSummariesCreate(CurrentSeasonSummariesBase):
    pass


class ICurrentSeasonSummariesRead(CurrentSeasonSummariesBase):
    id: UUID


# All these fields are optional
@optional
class ICurrentSeasonSummariesUpdate(CurrentSeasonSummariesBase):
    pass

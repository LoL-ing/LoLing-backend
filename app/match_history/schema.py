from app.match_history.model import MatchHistoriesBase
from uuid import UUID

from app.common.utils import optional


class IMatchHistoriesCreate(MatchHistoriesBase):
    pass


class IMatchHistoriesRead(MatchHistoriesBase):
    id: UUID


# All these fields are optional
@optional
class IMatchHistoriesUpdate(MatchHistoriesBase):
    pass

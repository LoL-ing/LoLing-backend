from sqlalchemy import (
    VARCHAR,
    Column,
    String,
    Text,
    Date,
    Integer,
    DateTime,
)
from db_connection.rds.orm import Base
from .base_model import BaseIdModel


class Match_histories(BaseIdModel):
    __tablename__ = "MATCH_HISTORIES"
    __table_args__ = {"schema": "MATCH_HISTORY"}
    level = Column(Integer, nullable=False,
                   comment='해당 match 내에서 user의 level을 나타낸다.')
    CS = Column(Integer, nullable=False,
                comment='creep score의 약자로, 해당 match에서 user가 미니언을 잡은 수 이다.')
    item_0_id = Column(Integer, nullable=False, default=0,
                       comment='해당 match에서 user의 첫번째 item칸에 있는 item의 고유 번호이다.')
    item_1_id = Column(Integer, nullable=False, default=0,
                       comment='해당 match에서 user의 두번째 item칸에 있는 item의 고유 번호이다.')
    item_2_id = Column(Integer, nullable=False, default=0)
    item_3_id = Column(Integer, nullable=False, default=0)
    item_4_id = Column(Integer, nullable=False, default=0)
    item_5_id = Column(Integer, nullable=False, default=0)
    item_6_id = Column(Integer, nullable=False, default=0)
    spell_0_id = Column(Integer, nullable=False, default=0,
                        comment='해당 match에서 user가 사용한 첫 번째 spell의 고유 번호이다.')
    spell_1_id = Column(Integer, nullable=False, default=0)
    rune_0_id = Column(Integer, nullable=False, default=0,
                       comment='해당 match에서 user가 사용한 첫 번째 rune의 고유 번호이다.')
    rune_1_id = Column(Integer, nullable=False, default=0)
    season = Column(String(20), nullable=False,
                    comment='match가 발생한 season을 나타낸다. 어느 season에서 발생한 것인지 알 수 있다.')
    gold = Column(Integer, nullable=False,
                  comment='해당 match에서 user가 획득한 총 gold 양이다.')
    play_duration = Column(Text, nullable=False,
                           comment='match의 play 총 시간이다. ')
    play_time = Column(Text, nullable=False, comment='match가 발생한 날짜 정보이다.')
    queue_type = Column(Integer, nullable=False,
                        comment='해당 match의 type(자유 랭크인지 솔로 랭크인지) 에 대한 고유 번호이다.')
    summoner_name = Column(String(20), nullable=False,
                           comment='각 match의 참여한 개별 소환사의 이름을 나타낸다.')
    match_id = Column(String(10), nullable=False,
                      comment='라이엇 API 가 제공하는 해당 match 의 고유 번호이다.')
    line_name = Column(String(20), nullable=False,
                       comment='해당 match에서 user가 플레이한 line 이름이다. ')
    champion_name_en = Column(
        String(20), nullable=False, comment='해당 match에서 user가 플레이한 champion 이름이다.')
    kill = Column(Integer, nullable=False,
                  comment='해당 match에서 user가 kill한 횟수이다.')
    death = Column(Integer, nullable=False,
                   comment='해당 match에서 user가 death한 횟수이다.')
    assist = Column(Integer, nullable=False,
                    comment='해당 mathc에서 user가 assist한 횟수이다.')
    win_or_lose = Column(Integer, nullable=False,
                         comment='해당 match에서 user가 이겼는지 졌는지를 나타내는 요소이다.')


class Current_season_summaries(BaseIdModel):
    __tablename__ = "CURRENT_SEASON_SUMMARIES"
    __table_args__ = {"schema": "MATCH_HISTORY"}
    losses = Column(Integer, nullable=False, default=0,
                    comment='해당 current season summary의 시즌 전체 패배 횟수이다.')
    lp = Column(Integer, unique=True, nullable=False, default=0,
                comment='해당 current season summary의 league point이다.')
    queue_id = Column(Integer, nullable=False,
                      comment='해당 Season Summary가 속한 queue 유형의 고유 번호이다.')
    rank = Column(Integer, nullable=False,
                  comment='해당 Current Season Summary의 tier를 세분화한 단계이다. ( I ~ IV )')
    summoner_id = Column(String(47), unique=True, nullable=False,
                         comment='라이엇 API에서 제공하는 소환사를 구별하기 위한 고유 번호. 라이엇 API의 league 정보를 불러오는데 쓰이는 고유번호이다.  해당 Current Season Summary의 소환사를 가리킨다.')
    tier_id = Column(Integer, nullable=False,
                     comment='해당 Season Summary가 속한 tier의 고유 번호이다.')
    wins = Column(Integer, nullable=False,
                  comment='해당 current season summary의 시즌 전체 승리 횟수이다.')

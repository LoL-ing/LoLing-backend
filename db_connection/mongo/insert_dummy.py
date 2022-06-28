from db_connection.mongo import get_db_connection
db = get_db_connection()
obj = {
    "Friends" : [
  {
    "nickname": '하아아아푸움',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Iron 4',
    "line": 'top',
  },

  {
    "nickname": '개란말이개미',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'mid',
  },

  {
    "nickname": '모닝글라스',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'bottom',
  },

  {
    "nickname": '부실멘탈',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'support',
  },

  {
    "nickname": '고려대김자헌',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'jungle',
  },

  {
    "nickname": '겨드랑이에낀손',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'jungle',
  },

  {
    "nickname": '즐거운프리핸드',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'mid',
  },

  {
    "nickname": '웰시코기궁둥이',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'support',
  },

  {
    "nickname": '불꽃근력마초보이',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'top',
  },

  {
    "nickname": '김수돌',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'support',
  },

  {
    "nickname": '리븐의신리신',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'jungle',
  },

  {
    "nickname": '후리스와청바지',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'bottom',
  },

  {
    "nickname": '따뜻한날씨',
    "profileImg": '../assets/images/Irelia.png',
    "tier": 'Diamond 4',
    "line": 'mid',
  },
],
 "Profiles" :[{
        "nickname": 'Soodoll',
        "tier": 'Gold 3',
        "winrate": '59%',
        "KDA": '3.87',
        "champ1Winrate": '57%',
        "champ2Winrate": '100%',
        "champ3Winrate": '85%',
        "champ1KDA": '3.87',
        "champ2KDA": '3.87',
        "champ3KDA": '3.87',
        "line1Winrate": '85%',
        "line2Winrate": '85%',
        "line1KDA": '3.87',
        "line2KDA": '3.87',
        "profileImg": '../assets/images/Irelia.png',
    },
    {
        "nickname": 'summerbonobono',
        "tier": 'Silver 4',
        "winrate": '59%',
        "KDA": '3.87',
        "champ1Winrate": '57%',
        "champ2Winrate": '100%',
        "champ3Winrate": '85%',
        "champ1KDA": '3.87',
        "champ2KDA": '3.87',
        "champ3KDA": '3.87',
        "line1Winrate": '85%',
        "line2Winrate": '85%',
        "line1KDA": '3.87',
        "line2KDA": '3.87',
        "profileImg": '../assets/images/Irelia.png',
    }],
    "Champions":[{
        "champImg": '../assets/images/Irelia.png',
        "champName": '갈리오',
        "champRole": '탱커',
    },

    {
        "champImg": '../assets/images/Irelia.png',
        "champName": '그레이브즈',
        "champRole": '원거리 딜러',
    },

    {
        "champImg": '../assets/images/Irelia.png',
        "champName": '그웬',
        "champRole": '암살자',
    },

    {
        "champImg": '../assets/images/Irelia.png',
        "champName": '드레이븐',
        "champRole": '원거리 딜러',
    },

    {
        "champImg": '../assets/images/Irelia.png',
        "champName": '럭스',
        "champRole": '마법사',
    },

    {
        "champImg": '../assets/images/Irelia.png',
        "champName": '루시안',
        "champRole": '원거리 딜러',
    },

    {
        "champImg": '../assets/images/Irelia.png',
        "champName": '룰루',
        "champRole": '서포터',
    },

    {
        "champImg": '../assets/images/Irelia.png',
        "champName": '미스 포춘',
        "champRole": '원거리 딜러',
    },

    {
        "champImg": '../assets/images/Irelia.png',
        "champName": '바루스',
        "champRole": '원거리 딜러',
    },

    {
        "champImg": '../assets/images/Irelia.png',
        "champName": '베인',
        "champRole": '원거리 딜러',
    },]


}

for table_nm in ['Friends', 'Champions', 'Profiles']:
    db[table_nm].insert_many(obj.get(table_nm))    

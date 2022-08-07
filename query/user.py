# 유저 정보 조회
SELECT_USER = """
    SELECT *
      FROM USER
     WHERE signin_id = %(user_id)s
    ;
    """

# 유저 정보 등록 -- 최초 회원가입 시
INSERT_USER_REGISER = """
    INSERT INTO LoLing.USER(
        signin_id,
        password,
        manner_tier,
        like_cnt,
        hate_cnt,
        created_at,
        updated_at
    ) VALUES(
        %(email)s,
        %(password)s,
        '골드',
        0,
        0,
        now(),
        null
    )
    """
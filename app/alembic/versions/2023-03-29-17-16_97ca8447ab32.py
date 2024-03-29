"""empty message

Revision ID: 97ca8447ab32
Revises: 
Create Date: 2023-03-29 17:16:50.256080

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision = '97ca8447ab32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ATTACHMENTS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(length=203), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('ATTACHMENTS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ATTACHMENTS_id'), ['id'], unique=False)

    op.create_table('BOARDS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description'),
    sa.UniqueConstraint('title')
    )
    with op.batch_alter_table('BOARDS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_BOARDS_id'), ['id'], unique=False)

    op.create_table('CHAMPIONS',
    sa.Column('name_en', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('name_kr', sqlmodel.sql.sqltypes.AutoString(length=15), nullable=False),
    sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(length=2083), nullable=True),
    sa.PrimaryKeyConstraint('name_en'),
    sa.UniqueConstraint('name_en'),
    sa.UniqueConstraint('name_kr')
    )
    op.create_table('COMMENTS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('like', sa.Integer(), nullable=False),
    sa.Column('parent_comment_id', sa.Integer(), nullable=False),
    sa.Column('parent_post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('COMMENTS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_COMMENTS_id'), ['id'], unique=False)

    op.create_table('CURRENT_SEASON_SUMMARIES',
    sa.Column('losses', sa.Integer(), nullable=False),
    sa.Column('lp', sa.Integer(), nullable=False),
    sa.Column('queue_id', sa.Integer(), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('summoner_id', sqlmodel.sql.sqltypes.AutoString(length=47), nullable=False),
    sa.Column('puu_id', sqlmodel.sql.sqltypes.AutoString(length=78), nullable=False),
    sa.Column('tier_id', sa.Integer(), nullable=False),
    sa.Column('wins', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('puu_id', 'id'),
    sa.UniqueConstraint('lp')
    )
    with op.batch_alter_table('CURRENT_SEASON_SUMMARIES', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_CURRENT_SEASON_SUMMARIES_id'), ['id'], unique=False)

    op.create_table('ITEMS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(length=2083), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('ITEMS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ITEMS_id'), ['id'], unique=False)

    op.create_table('LINES',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=False),
    sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(length=2083), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('LOL_PROFILES',
    sa.Column('puu_id', sqlmodel.sql.sqltypes.AutoString(length=78), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('profile_icon_id', sa.Integer(), nullable=False),
    sa.Column('region', sqlmodel.sql.sqltypes.AutoString(length=5), nullable=False),
    sa.Column('summoner_id', sqlmodel.sql.sqltypes.AutoString(length=47), nullable=False),
    sa.Column('summoner_level', sa.Integer(), nullable=False),
    sa.Column('summoner_name', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('last_updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('puu_id'),
    sa.UniqueConstraint('summoner_id')
    )
    op.create_table('MATCH_HISTORIES',
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('CS', sa.Integer(), nullable=False),
    sa.Column('item_0_id', sa.Integer(), nullable=False),
    sa.Column('item_1_id', sa.Integer(), nullable=False),
    sa.Column('item_2_id', sa.Integer(), nullable=False),
    sa.Column('item_3_id', sa.Integer(), nullable=False),
    sa.Column('item_4_id', sa.Integer(), nullable=False),
    sa.Column('item_5_id', sa.Integer(), nullable=False),
    sa.Column('item_6_id', sa.Integer(), nullable=False),
    sa.Column('spell_0_id', sa.Integer(), nullable=False),
    sa.Column('spell_1_id', sa.Integer(), nullable=False),
    sa.Column('rune_0_id', sa.Integer(), nullable=False),
    sa.Column('rune_1_id', sa.Integer(), nullable=False),
    sa.Column('season', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('gold', sa.Integer(), nullable=False),
    sa.Column('play_duration', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('play_time', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('queue_type', sa.Integer(), nullable=False),
    sa.Column('summoner_name', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('match_id', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('line_name', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('champion_name_en', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('kill', sa.Integer(), nullable=False),
    sa.Column('death', sa.Integer(), nullable=False),
    sa.Column('assist', sa.Integer(), nullable=False),
    sa.Column('win_or_lose', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('MATCH_HISTORIES', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_MATCH_HISTORIES_id'), ['id'], unique=False)

    op.create_table('MOST_CHAMPION_SUMMARIES',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('current_season_summary_id', sa.Integer(), nullable=False),
    sa.Column('champion_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('kda', sa.Float(), nullable=False),
    sa.Column('win_rate', sa.Float(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('MOST_CHAMPION_SUMMARIES', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_MOST_CHAMPION_SUMMARIES_id'), ['id'], unique=False)

    op.create_table('MOST_LINE_SUMMARIES',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('current_season_summary_id', sa.Integer(), nullable=False),
    sa.Column('line_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('kda', sa.Float(), nullable=False),
    sa.Column('win_rate', sa.Float(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('MOST_LINE_SUMMARIES', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_MOST_LINE_SUMMARIES_id'), ['id'], unique=False)

    op.create_table('POSTS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('like', sa.Integer(), nullable=False),
    sa.Column('scrap', sa.Integer(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('view', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('POSTS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_POSTS_id'), ['id'], unique=False)

    op.create_table('PROFILE_ICONS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(length=2083), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('PROFILE_ICONS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_PROFILE_ICONS_id'), ['id'], unique=False)

    op.create_table('QUEUES',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type')
    )
    with op.batch_alter_table('QUEUES', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_QUEUES_id'), ['id'], unique=False)

    op.create_table('RELATIONSHIPS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('accepted', sa.Integer(), nullable=False),
    sa.Column('from_user_id', sa.Integer(), nullable=False),
    sa.Column('message_id', sqlmodel.sql.sqltypes.AutoString(length=24), nullable=False),
    sa.Column('to_user_id', sa.Integer(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('message_id')
    )
    with op.batch_alter_table('RELATIONSHIPS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_RELATIONSHIPS_id'), ['id'], unique=False)

    op.create_table('REPORTED_COMMENTS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('reported_comment_id', sa.Integer(), nullable=False),
    sa.Column('reporter_user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('REPORTED_COMMENTS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_REPORTED_COMMENTS_id'), ['id'], unique=False)

    op.create_table('REPORTED_POSTS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('reported_post_id', sa.Integer(), nullable=False),
    sa.Column('reporter_user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('REPORTED_POSTS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_REPORTED_POSTS_id'), ['id'], unique=False)

    op.create_table('REPORTED_USERS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('reported_user_id', sa.Integer(), nullable=False),
    sa.Column('reporter_user_id', sa.Integer(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('REPORTED_USERS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_REPORTED_USERS_id'), ['id'], unique=False)

    op.create_table('RUNES',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(length=2083), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('RUNES', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_RUNES_id'), ['id'], unique=False)

    op.create_table('SCHOOLS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=25), nullable=False),
    sa.Column('school_type', sqlmodel.sql.sqltypes.AutoString(length=1), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('SCHOOLS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_SCHOOLS_id'), ['id'], unique=False)

    op.create_table('SPELLS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(length=2083), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('SPELLS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_SPELLS_id'), ['id'], unique=False)

    op.create_table('TIERS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('image_url', sqlmodel.sql.sqltypes.AutoString(length=2083), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('TIERS', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_TIERS_id'), ['id'], unique=False)

    op.create_table('USERS',
    sa.Column('signin_id', sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=False),
    sa.Column('self_desc', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
    sa.Column('phone_num', sqlmodel.sql.sqltypes.AutoString(length=11), nullable=False),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
    sa.Column('manner_tier', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=True),
    sa.Column('curr_lol_account', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
    sa.Column('like_cnt', sa.Integer(), nullable=False),
    sa.Column('hate_cnt', sa.Integer(), nullable=False),
    sa.Column('profile_image_uri', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['school_id'], ['SCHOOLS.id'], ),
    sa.PrimaryKeyConstraint('signin_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('USERS')
    with op.batch_alter_table('TIERS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_TIERS_id'))

    op.drop_table('TIERS')
    with op.batch_alter_table('SPELLS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_SPELLS_id'))

    op.drop_table('SPELLS')
    with op.batch_alter_table('SCHOOLS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_SCHOOLS_id'))

    op.drop_table('SCHOOLS')
    with op.batch_alter_table('RUNES', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_RUNES_id'))

    op.drop_table('RUNES')
    with op.batch_alter_table('REPORTED_USERS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_REPORTED_USERS_id'))

    op.drop_table('REPORTED_USERS')
    with op.batch_alter_table('REPORTED_POSTS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_REPORTED_POSTS_id'))

    op.drop_table('REPORTED_POSTS')
    with op.batch_alter_table('REPORTED_COMMENTS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_REPORTED_COMMENTS_id'))

    op.drop_table('REPORTED_COMMENTS')
    with op.batch_alter_table('RELATIONSHIPS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_RELATIONSHIPS_id'))

    op.drop_table('RELATIONSHIPS')
    with op.batch_alter_table('QUEUES', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_QUEUES_id'))

    op.drop_table('QUEUES')
    with op.batch_alter_table('PROFILE_ICONS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_PROFILE_ICONS_id'))

    op.drop_table('PROFILE_ICONS')
    with op.batch_alter_table('POSTS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_POSTS_id'))

    op.drop_table('POSTS')
    with op.batch_alter_table('MOST_LINE_SUMMARIES', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_MOST_LINE_SUMMARIES_id'))

    op.drop_table('MOST_LINE_SUMMARIES')
    with op.batch_alter_table('MOST_CHAMPION_SUMMARIES', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_MOST_CHAMPION_SUMMARIES_id'))

    op.drop_table('MOST_CHAMPION_SUMMARIES')
    with op.batch_alter_table('MATCH_HISTORIES', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_MATCH_HISTORIES_id'))

    op.drop_table('MATCH_HISTORIES')
    op.drop_table('LOL_PROFILES')
    op.drop_table('LINES')
    with op.batch_alter_table('ITEMS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_ITEMS_id'))

    op.drop_table('ITEMS')
    with op.batch_alter_table('CURRENT_SEASON_SUMMARIES', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_CURRENT_SEASON_SUMMARIES_id'))

    op.drop_table('CURRENT_SEASON_SUMMARIES')
    with op.batch_alter_table('COMMENTS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_COMMENTS_id'))

    op.drop_table('COMMENTS')
    op.drop_table('CHAMPIONS')
    with op.batch_alter_table('BOARDS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_BOARDS_id'))

    op.drop_table('BOARDS')
    with op.batch_alter_table('ATTACHMENTS', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_ATTACHMENTS_id'))

    op.drop_table('ATTACHMENTS')
    # ### end Alembic commands ###

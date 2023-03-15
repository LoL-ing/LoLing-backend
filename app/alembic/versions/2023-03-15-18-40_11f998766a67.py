"""empty message

Revision ID: 11f998766a67
Revises: a355300849ef
Create Date: 2023-03-15 18:40:56.524902

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '11f998766a67'
down_revision = 'a355300849ef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('MOST_CHAMPION_SUMMARIES', schema=None) as batch_op:
        batch_op.add_column(sa.Column('champion_name_en', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.drop_column('champion_id')

    with op.batch_alter_table('MOST_LINE_SUMMARIES', schema=None) as batch_op:
        batch_op.add_column(sa.Column('line_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.drop_column('line_id')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('MOST_LINE_SUMMARIES', schema=None) as batch_op:
        batch_op.add_column(sa.Column('line_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('line_name')

    with op.batch_alter_table('MOST_CHAMPION_SUMMARIES', schema=None) as batch_op:
        batch_op.add_column(sa.Column('champion_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('champion_name_en')

    # ### end Alembic commands ###

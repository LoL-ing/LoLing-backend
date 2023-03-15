"""empty message

Revision ID: a355300849ef
Revises: 15b6e68c4783
Create Date: 2023-03-15 18:36:52.534232

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a355300849ef'
down_revision = '15b6e68c4783'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('CHAMPIONS', schema=None) as batch_op:
        batch_op.drop_index('ix_CHAMPIONS_id')
        batch_op.drop_column('created_at')
        batch_op.drop_column('id')
        batch_op.drop_column('updated_at')

    with op.batch_alter_table('LINES', schema=None) as batch_op:
        batch_op.drop_index('ix_LINES_id')
        batch_op.drop_column('created_at')
        batch_op.drop_column('id')
        batch_op.drop_column('updated_at')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('LINES', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', mysql.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('created_at', mysql.DATETIME(), nullable=False))
        batch_op.create_index('ix_LINES_id', ['id'], unique=False)

    with op.batch_alter_table('CHAMPIONS', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', mysql.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.add_column(sa.Column('created_at', mysql.DATETIME(), nullable=False))
        batch_op.create_index('ix_CHAMPIONS_id', ['id'], unique=False)

    # ### end Alembic commands ###

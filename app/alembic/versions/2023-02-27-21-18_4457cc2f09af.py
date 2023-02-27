"""empty message

Revision ID: 4457cc2f09af
Revises: 2496c9b62ff2
Create Date: 2023-02-27 21:18:48.698818

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4457cc2f09af'
down_revision = '2496c9b62ff2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('RELATIONSHIPS', schema=None) as batch_op:
        batch_op.drop_column('test')

    with op.batch_alter_table('SPELLS', schema=None) as batch_op:
        batch_op.drop_column('test')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('SPELLS', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test', mysql.VARCHAR(length=255), nullable=False))

    with op.batch_alter_table('RELATIONSHIPS', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test', mysql.VARCHAR(length=255), nullable=False))

    # ### end Alembic commands ###

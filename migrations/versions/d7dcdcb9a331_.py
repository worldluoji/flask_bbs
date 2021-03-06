"""empty message

Revision ID: d7dcdcb9a331
Revises: f54be764c408
Create Date: 2018-10-29 10:24:13.175454

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd7dcdcb9a331'
down_revision = 'f54be764c408'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('administrator', sa.Column('_password', sa.String(length=100), nullable=False))
    op.drop_column('administrator', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('administrator', sa.Column('password', mysql.VARCHAR(length=100), nullable=False))
    op.drop_column('administrator', '_password')
    # ### end Alembic commands ###

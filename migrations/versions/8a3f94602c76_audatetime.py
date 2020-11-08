"""auDateTime.

Revision ID: 8a3f94602c76
Revises: 8d8f5df58df8
Create Date: 2020-11-05 13:19:57.026793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a3f94602c76'
down_revision = '8d8f5df58df8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auto', sa.Column('auend_of_rent', sa.DateTime(), nullable=True))
    op.add_column('auto', sa.Column('aurented', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('auto', 'aurented')
    op.drop_column('auto', 'auend_of_rent')
    # ### end Alembic commands ###
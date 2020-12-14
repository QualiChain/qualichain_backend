"""empty message

Revision ID: 1af979f03503
Revises: 76df844724d1
Create Date: 2020-12-11 16:49:47.064269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1af979f03503'
down_revision = '76df844724d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('thesis', sa.Column('status', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('thesis', 'status')
    # ### end Alembic commands ###

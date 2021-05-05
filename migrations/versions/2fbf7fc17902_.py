"""empty message

Revision ID: 2fbf7fc17902
Revises: 96df4e739c2d
Create Date: 2021-05-05 16:35:39.415641

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2fbf7fc17902'
down_revision = '96df4e739c2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jobs', 'employment_value')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('employment_value', postgresql.ENUM('part_time', 'full_time', 'contractor', 'freelance', name='employmenttype'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

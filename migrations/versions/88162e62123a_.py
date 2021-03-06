"""empty message

Revision ID: 88162e62123a
Revises: 9d8e0a452567
Create Date: 2020-11-09 18:34:14.556073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88162e62123a'
down_revision = '9d8e0a452567'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('specialization_id', sa.Integer(), nullable=True))
    op.drop_constraint('jobs_specialization_fkey', 'jobs', type_='foreignkey')
    op.create_foreign_key(None, 'jobs', 'specialization', ['specialization_id'], ['id'])
    op.drop_column('jobs', 'specialization')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jobs', sa.Column('specialization', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'jobs', type_='foreignkey')
    op.create_foreign_key('jobs_specialization_fkey', 'jobs', 'specialization', ['specialization'], ['id'])
    op.drop_column('jobs', 'specialization_id')
    # ### end Alembic commands ###

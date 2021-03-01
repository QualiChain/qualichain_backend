"""empty message

Revision ID: a709582f1482
Revises: dea77127e15e
Create Date: 2020-12-14 15:12:31.392124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a709582f1482'
down_revision = '88162e62123a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('thesis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('professor_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['professor_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('smart_badges', sa.Column('type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('smart_badges', 'type')
    op.drop_table('thesis')
    # ### end Alembic commands ###

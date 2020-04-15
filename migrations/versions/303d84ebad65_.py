"""empty message

Revision ID: 303d84ebad65
Revises: 
Create Date: 2020-04-15 11:43:30.684493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '303d84ebad65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('published', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('semester', sa.String(), nullable=True),
    sa.Column('endDate', sa.String(), nullable=True),
    sa.Column('startDate', sa.String(), nullable=True),
    sa.Column('updatedDate', sa.String(), nullable=True),
    sa.Column('skills', sa.JSON(), nullable=True),
    sa.Column('events', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('job_description', sa.String(), nullable=True),
    sa.Column('level', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('start_date', sa.String(), nullable=True),
    sa.Column('end_date', sa.String(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('employment_type', sa.String(), nullable=True),
    sa.Column('skills', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('skills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userPath', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('pilotId', sa.Integer(), nullable=True),
    sa.Column('userName', sa.String(), nullable=True),
    sa.Column('fullName', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('birthDate', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('zipCode', sa.String(), nullable=True),
    sa.Column('mobilePhone', sa.String(), nullable=True),
    sa.Column('homePhone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('course_status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('available', sa.String(), nullable=True),
    sa.Column('exp_salary', sa.String(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_jobs')
    op.drop_table('user_courses')
    op.drop_table('users')
    op.drop_table('skills')
    op.drop_table('jobs')
    op.drop_table('courses')
    op.drop_table('books')
    # ### end Alembic commands ###

"""init

Revision ID: 255fa0a6b2d2
Revises: 
Create Date: 2023-03-08 14:04:00.620721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '255fa0a6b2d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('user_password', sa.String(), nullable=False),
    sa.Column('user_email', sa.String(), nullable=False),
    sa.Column('user_status', sa.String(), nullable=True),
    sa.Column('user_registred_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user_email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
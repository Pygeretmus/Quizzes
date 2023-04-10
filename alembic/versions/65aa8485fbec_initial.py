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
    sa.Column('user_registred_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user_email')
    )
    op.create_table('Companies',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(), nullable=False),
    sa.Column('company_description', sa.String(), nullable=True),
    sa.Column('company_owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_owner_id'], ['Users.user_id']),
    sa.PrimaryKeyConstraint('company_id')
    )
    op.create_table('Statistics',
    sa.Column('statistic_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('quiz_questions', sa.Integer(), nullable=False),
    sa.Column('quiz_right_answers', sa.Integer(), nullable=False),
    sa.Column('quiz_average', sa.Float(), nullable=False),
    sa.Column('quizzes_questions', sa.Integer(), nullable=False),
    sa.Column('quizzes_right_answers', sa.Integer(), nullable=False),
    sa.Column('quizzes_average', sa.Float(), nullable=False),
    sa.Column('company_questions', sa.Integer(), nullable=False),
    sa.Column('company_right_answers', sa.Integer(), nullable=False),
    sa.Column('company_average', sa.Float(), nullable=False),
    sa.Column('all_questions', sa.Integer(), nullable=False),
    sa.Column('all_right_answers', sa.Integer(), nullable=False),
    sa.Column('all_average', sa.Float(), nullable=False),
    sa.Column('quiz_passed_at', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['Users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('statistic_id')
    )
    op.create_table('Invites',
    sa.Column('invite_id', sa.Integer(), nullable=False),
    sa.Column('to_user_id', sa.Integer(), nullable=False),
    sa.Column('from_company_id', sa.Integer(), nullable=False),
    sa.Column('invite_message', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['from_company_id'], ['Companies.company_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_user_id'], ['Users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('invite_id')
    )
    op.create_table('Members',
    sa.Column('useless_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['Companies.company_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('useless_id')
    )
    op.create_table('Quizzes',
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('quiz_name', sa.String(), nullable=False),
    sa.Column('quiz_frequency', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['Companies.company_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('quiz_id')
    )
    op.create_table('Requests',
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('to_company_id', sa.Integer(), nullable=False),
    sa.Column('from_user_id', sa.Integer(), nullable=False),
    sa.Column('request_message', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['from_user_id'], ['Users.user_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_company_id'], ['Companies.company_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('request_id')
    )
    op.create_table('Notifications',
    sa.Column('notification_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('notification_time', sa.DateTime(), nullable=False),
    sa.Column('notification_read', sa.Boolean(), nullable=False),
    sa.Column('notification_content', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['Companies.company_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['quiz_id'], ['Quizzes.quiz_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['Users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('notification_id')
    )
    op.create_table('Questions',
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('question_name', sa.String(), nullable=False),
    sa.Column('question_answers', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('question_right', sa.String(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['Quizzes.quiz_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('question_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Questions')
    op.drop_table('Notifications')
    op.drop_table('Requests')
    op.drop_table('Quizzes')
    op.drop_table('Members')
    op.drop_table('Invites')
    op.drop_table('Statistics')
    op.drop_table('Companies')
    op.drop_table('Users')
    # ### end Alembic commands ###

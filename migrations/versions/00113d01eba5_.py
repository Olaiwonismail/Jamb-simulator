"""empty message

Revision ID: 00113d01eba5
Revises: 768cfc997be2
Create Date: 2024-11-30 21:12:05.818322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00113d01eba5'
down_revision = '768cfc997be2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users')
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.alter_column('subject',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.alter_column('question_text',
               existing_type=sa.TEXT(),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.alter_column('option_a',
               existing_type=sa.TEXT(),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.alter_column('option_b',
               existing_type=sa.TEXT(),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.alter_column('option_c',
               existing_type=sa.TEXT(),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.alter_column('option_d',
               existing_type=sa.TEXT(),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.alter_column('correct_option',
               existing_type=sa.VARCHAR(length=1),
               type_=sa.String(length=64),
               existing_nullable=False)

    with op.batch_alter_table('score_details', schema=None) as batch_op:
        batch_op.alter_column('question_text',
               existing_type=sa.TEXT(),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.alter_column('user_answer',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=64),
               existing_nullable=True)
        batch_op.alter_column('correct_answer',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=64),
               existing_nullable=False)

    with op.batch_alter_table('scores', schema=None) as batch_op:
        batch_op.alter_column('subject',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scores', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.alter_column('subject',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    with op.batch_alter_table('score_details', schema=None) as batch_op:
        batch_op.alter_column('correct_answer',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False)
        batch_op.alter_column('user_answer',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)
        batch_op.alter_column('question_text',
               existing_type=sa.String(length=64),
               type_=sa.TEXT(),
               existing_nullable=False)

    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.alter_column('correct_option',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=1),
               existing_nullable=False)
        batch_op.alter_column('option_d',
               existing_type=sa.String(length=64),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('option_c',
               existing_type=sa.String(length=64),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('option_b',
               existing_type=sa.String(length=64),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('option_a',
               existing_type=sa.String(length=64),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('question_text',
               existing_type=sa.String(length=64),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('subject',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=150), nullable=False),
    sa.Column('email', sa.VARCHAR(length=150), nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.drop_table('user')
    # ### end Alembic commands ###

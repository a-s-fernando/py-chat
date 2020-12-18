"""initial

Revision ID: 28a43e31c5aa
Revises: 
Create Date: 2020-12-18 00:53:58.771920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28a43e31c5aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friend',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('friendid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('groupname', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('groupid', sa.Integer(), nullable=True),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('senderid', sa.Integer(), nullable=True),
    sa.Column('recipientid', sa.Integer(), nullable=True),
    sa.Column('groupid', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('message', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('requesterid', sa.Integer(), nullable=True),
    sa.Column('requestedid', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('request')
    op.drop_table('message')
    op.drop_table('member')
    op.drop_table('group')
    op.drop_table('friend')
    # ### end Alembic commands ###

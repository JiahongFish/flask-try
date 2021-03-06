"""empty message

Revision ID: fff66f5ed9aa
Revises: 
Create Date: 2018-03-12 15:03:20.639601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fff66f5ed9aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('firstname', sa.String(length=100), nullable=False),
    sa.Column('lastname', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###

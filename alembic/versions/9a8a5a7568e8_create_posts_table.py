"""create posts table

Revision ID: 9a8a5a7568e8
Revises: 
Create Date: 2022-07-11 10:49:14.169354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a8a5a7568e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable= False, primary_key = True), sa.Column('title', sa.String(), nullable= False))
    pass


def downgrade():
    op.drop_table('posts')
    pass

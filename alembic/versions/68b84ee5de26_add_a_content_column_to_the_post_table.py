"""add a content column to the post table

Revision ID: 68b84ee5de26
Revises: 9a8a5a7568e8
Create Date: 2022-07-11 11:46:45.777591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68b84ee5de26'
down_revision = '9a8a5a7568e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

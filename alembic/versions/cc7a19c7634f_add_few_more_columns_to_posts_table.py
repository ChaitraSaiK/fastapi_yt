"""add few more columns to posts table

Revision ID: cc7a19c7634f
Revises: 8c111e1b5daa
Create Date: 2022-07-11 12:57:00.700897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc7a19c7634f'
down_revision = '8c111e1b5daa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable = False, server_default= 'TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone = True),  nullable = False, server_default= sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass

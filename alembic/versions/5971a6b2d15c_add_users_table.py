"""add users table

Revision ID: 5971a6b2d15c
Revises: 68b84ee5de26
Create Date: 2022-07-11 12:11:19.969470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5971a6b2d15c'
down_revision = '68b84ee5de26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default= sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                     )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass

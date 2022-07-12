"""Add foreign key to posts table

Revision ID: 8c111e1b5daa
Revises: 5971a6b2d15c
Create Date: 2022-07-11 12:31:16.158599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c111e1b5daa'
down_revision = '5971a6b2d15c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_users_fk', source_table= 'posts', referent_table= 'users', local_cols= ['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass

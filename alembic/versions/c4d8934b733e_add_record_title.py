"""add record title

Revision ID: c4d8934b733e
Revises: 708a762f0724
Create Date: 2023-05-17 16:42:28.350157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4d8934b733e'
down_revision = '708a762f0724'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('records', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('records', 'title')
    # ### end Alembic commands ###

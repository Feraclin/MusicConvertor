"""Initial

Revision ID: 708a762f0724
Revises: 
Create Date: 2023-05-17 11:31:37.412766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "708a762f0724"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id_", sa.UUID(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("access_token", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id_"),
    )
    op.create_table(
        "records",
        sa.Column("id_", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("record_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id_"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id_"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("records")
    op.drop_table("users")
    # ### end Alembic commands ###

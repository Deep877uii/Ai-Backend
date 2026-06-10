"""add user table

Revision ID: fe356845f1b0
Revises: ff13a25aab9f
Create Date: 2026-06-07 20:02:38.832299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe356845f1b0'
down_revision: Union[str, Sequence[str], None] = 'ff13a25aab9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade():
    op.drop_table("user")
    pass

"""create Post table

Revision ID: ff13a25aab9f
Revises: 
Create Date: 2026-06-07 19:03:35.029659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff13a25aab9f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    op.create_table(
        "Post",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("publisher", sa.Boolean(), nullable=False, server_default='true'),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )
    pass


def downgrade():
    """Downgrade schema."""
    op.drop_table("Post")
    pass

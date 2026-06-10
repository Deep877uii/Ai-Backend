"""add auto-vote

Revision ID: 0d44732c0cc8
Revises: 7aa512092929
Create Date: 2026-06-07 20:30:36.728104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0d44732c0cc8'
down_revision: Union[str, Sequence[str], None] = '7aa512092929'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'vote',
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),

        sa.ForeignKeyConstraint(
            ['post_id'],
            ['Post.id'],
            ondelete='CASCADE'
        ),

        sa.ForeignKeyConstraint(
            ['user_id'],
            ['user.id'],
            ondelete='CASCADE'
        ),

        sa.PrimaryKeyConstraint('post_id', 'user_id')
    )

def downgrade() -> None:
    op.drop_table('vote')

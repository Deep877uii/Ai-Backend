"""add foreign-key to Post table

Revision ID: 7aa512092929
Revises: fe356845f1b0
Create Date: 2026-06-07 20:16:03.416391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7aa512092929'
down_revision: Union[str, Sequence[str], None] = 'fe356845f1b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    op.create_foreign_key(
        "post_users_fk", #ye name humne khud diya hai
        source_table="Post",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )
    pass


def downgrade():
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", table_name="Post")
    pass    


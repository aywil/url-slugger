"""create shortlinks table

Revision ID: 4e59a152906b
Revises:
Create Date: 2025-12-22 01:00:46.776489

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4e59a152906b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "short_links",
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("clicks", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("slug", name=op.f("pk_short_links")),
    )
    op.create_index(op.f("ix_short_links_slug"), "short_links", ["slug"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_short_links_slug"), table_name="short_links")
    op.drop_table("short_links")

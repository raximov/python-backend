"""move images to photo service

Revision ID: c91be6000001
Revises: ba0b9389b84f
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "c91be6000001"
down_revision: Union[str, Sequence[str], None] = "ba0b9389b84f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint(
        "products_image_id_fkey",
        "products",
        type_="foreignkey",
    )

    op.drop_table("images")


def downgrade() -> None:
    op.create_table(
        "images",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "image",
            sa.LargeBinary(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_foreign_key(
        "products_image_id_fkey",
        "products",
        "images",
        ["image_id"],
        ["id"],
        ondelete="SET NULL",
    )

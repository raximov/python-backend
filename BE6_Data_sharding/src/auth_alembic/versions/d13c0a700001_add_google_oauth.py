"""add google oauth

Revision ID: d13c0a700001
Revises: aa93607eead8
"""

from alembic import op
import sqlalchemy as sa


revision = "d13c0a700001"
down_revision = "aa93607eead8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "phone_number",
        existing_type=sa.String(length=32),
        nullable=True,
    )

    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        nullable=True,
    )

    op.add_column(
        "users",
        sa.Column(
            "google_sub",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_users_google_sub",
        "users",
        ["google_sub"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_users_google_sub",
        table_name="users",
    )

    op.drop_column("users", "google_sub")

    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        nullable=False,
    )

    op.alter_column(
        "users",
        "phone_number",
        existing_type=sa.String(length=32),
        nullable=False,
    )

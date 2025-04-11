"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2023-09-01

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create url_mappings table
    op.create_table(
        "url_mappings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("short_code", sa.String(), nullable=False),
        sa.Column("original_url", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("last_accessed", sa.DateTime(), nullable=True),
        sa.Column(
            "access_count", sa.Integer(), server_default=sa.text("0"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes
    op.create_index(op.f("ix_url_mappings_id"), "url_mappings", ["id"], unique=False)
    op.create_index(
        op.f("ix_url_mappings_short_code"), "url_mappings", ["short_code"], unique=True
    )


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f("ix_url_mappings_short_code"), table_name="url_mappings")
    op.drop_index(op.f("ix_url_mappings_id"), table_name="url_mappings")

    # Drop table
    op.drop_table("url_mappings")

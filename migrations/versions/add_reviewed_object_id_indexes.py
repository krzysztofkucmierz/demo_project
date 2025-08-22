"""
Add indexes on reviews.reviewed_object_id and (reviewed_object_id, created_at)

Revision ID: add_reviewed_object_id_indexes
Revises: 87e9b654863c
Create Date: 2025-08-22
"""

from alembic import op  # type: ignore
from sqlalchemy import text  # type: ignore

# revision identifiers, used by Alembic.
revision = "add_reviewed_object_id_indexes"
down_revision = "87e9b654863c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Get connection; indexes will be created within the current transaction (no CONCURRENTLY)
    connection = op.get_bind()

    # Create indexes without CONCURRENTLY since we're in a transaction
    # In production, these could be run manually with CONCURRENTLY
    connection.execute(
        text(
            "CREATE INDEX IF NOT EXISTS idx_reviews_reviewed_object_id "
            "ON reviews (reviewed_object_id);"
        )
    )
    connection.execute(
        text(
            "CREATE INDEX IF NOT EXISTS idx_reviews_object_created "
            "ON reviews (reviewed_object_id, created_at DESC);"
        )
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        text("DROP INDEX IF EXISTS idx_reviews_object_created;")
    )
    connection.execute(
        text("DROP INDEX IF EXISTS idx_reviews_reviewed_object_id;")
    )

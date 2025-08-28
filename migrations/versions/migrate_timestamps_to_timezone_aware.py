"""
Migrate timestamps to timezone-aware format

Revision ID: migrate_timestamps_to_timezone_aware
Revises: add_reviewed_object_id_indexes
Create Date: 2025-08-28

"""

from alembic import op  # type: ignore
from sqlalchemy import text  # type: ignore

# revision identifiers, used by Alembic.
revision = "migrate_timestamps_to_timezone_aware"
down_revision = "add_reviewed_object_id_indexes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Migrate all timestamp columns to timezone-aware format."""
    connection = op.get_bind()
    
    # Migrate reviewers table timestamp columns
    connection.execute(
        text(
            "ALTER TABLE reviewers "
            "ALTER COLUMN created_at TYPE timestamp with time zone, "
            "ALTER COLUMN updated_at TYPE timestamp with time zone;"
        )
    )
    
    # Migrate reviewed_objects table timestamp columns  
    connection.execute(
        text(
            "ALTER TABLE reviewed_objects "
            "ALTER COLUMN created_at TYPE timestamp with time zone, "
            "ALTER COLUMN updated_at TYPE timestamp with time zone;"
        )
    )
    
    # Migrate reviews table timestamp columns
    connection.execute(
        text(
            "ALTER TABLE reviews "
            "ALTER COLUMN created_at TYPE timestamp with time zone, "
            "ALTER COLUMN updated_at TYPE timestamp with time zone;"
        )
    )


def downgrade() -> None:
    """Revert timestamps back to non-timezone-aware format."""
    connection = op.get_bind()
    
    # Revert reviews table timestamp columns
    connection.execute(
        text(
            "ALTER TABLE reviews "
            "ALTER COLUMN created_at TYPE timestamp without time zone, "
            "ALTER COLUMN updated_at TYPE timestamp without time zone;"
        )
    )
    
    # Revert reviewed_objects table timestamp columns
    connection.execute(
        text(
            "ALTER TABLE reviewed_objects "
            "ALTER COLUMN created_at TYPE timestamp without time zone, "
            "ALTER COLUMN updated_at TYPE timestamp without time zone;"
        )
    )
    
    # Revert reviewers table timestamp columns
    connection.execute(
        text(
            "ALTER TABLE reviewers "
            "ALTER COLUMN created_at TYPE timestamp without time zone, "
            "ALTER COLUMN updated_at TYPE timestamp without time zone;"
        )
    )
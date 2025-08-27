"""migrate_timestamps_to_timezone_aware

Revision ID: f92328734279
Revises: add_reviewed_object_id_indexes
Create Date: 2025-08-27 17:48:47.164384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f92328734279'
down_revision: Union[str, Sequence[str], None] = 'add_reviewed_object_id_indexes'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Convert all timestamp columns from 'timestamp without time zone' to 'timestamp with time zone'
    # This assumes existing data is in UTC (server default is NOW() which returns UTC in PostgreSQL)
    
    # Update reviewers table timestamp columns
    op.alter_column(
        "reviewers", "created_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="created_at AT TIME ZONE 'UTC'"
    )
    op.alter_column(
        "reviewers", "updated_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="updated_at AT TIME ZONE 'UTC'"
    )
    
    # Update reviewed_objects table timestamp columns
    op.alter_column(
        "reviewed_objects", "created_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="created_at AT TIME ZONE 'UTC'"
    )
    op.alter_column(
        "reviewed_objects", "updated_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="updated_at AT TIME ZONE 'UTC'"
    )
    
    # Update reviews table timestamp columns
    op.alter_column(
        "reviews", "created_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="created_at AT TIME ZONE 'UTC'"
    )
    op.alter_column(
        "reviews", "updated_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="updated_at AT TIME ZONE 'UTC'"
    )
    
    # Update default values to use timezone-aware functions
    op.alter_column(
        "reviewers", "created_at",
        server_default=sa.text("CURRENT_TIMESTAMP")
    )
    op.alter_column(
        "reviewers", "updated_at",
        server_default=sa.text("CURRENT_TIMESTAMP")
    )
    op.alter_column(
        "reviewed_objects", "created_at",
        server_default=sa.text("CURRENT_TIMESTAMP")
    )
    op.alter_column(
        "reviewed_objects", "updated_at",
        server_default=sa.text("CURRENT_TIMESTAMP")
    )
    op.alter_column(
        "reviews", "created_at",
        server_default=sa.text("CURRENT_TIMESTAMP")
    )
    op.alter_column(
        "reviews", "updated_at",
        server_default=sa.text("CURRENT_TIMESTAMP")
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert back to timestamp without time zone
    # Convert timezone-aware timestamps back to naive timestamps (assumes UTC)
    
    # Revert default values first
    op.execute("ALTER TABLE reviewers ALTER COLUMN created_at SET DEFAULT NOW()")
    op.execute("ALTER TABLE reviewers ALTER COLUMN updated_at SET DEFAULT NOW()")
    op.execute("ALTER TABLE reviewed_objects ALTER COLUMN created_at SET DEFAULT NOW()")
    op.execute("ALTER TABLE reviewed_objects ALTER COLUMN updated_at SET DEFAULT NOW()")
    op.execute("ALTER TABLE reviews ALTER COLUMN created_at SET DEFAULT NOW()")
    op.execute("ALTER TABLE reviews ALTER COLUMN updated_at SET DEFAULT NOW()")
    
    # Revert reviewers table timestamp columns
    op.execute("ALTER TABLE reviewers ALTER COLUMN created_at TYPE timestamp without time zone USING created_at AT TIME ZONE 'UTC'")
    op.execute("ALTER TABLE reviewers ALTER COLUMN updated_at TYPE timestamp without time zone USING updated_at AT TIME ZONE 'UTC'")
    
    # Revert reviewed_objects table timestamp columns
    op.execute("ALTER TABLE reviewed_objects ALTER COLUMN created_at TYPE timestamp without time zone USING created_at AT TIME ZONE 'UTC'")
    op.execute("ALTER TABLE reviewed_objects ALTER COLUMN updated_at TYPE timestamp without time zone USING updated_at AT TIME ZONE 'UTC'")
    
    # Revert reviews table timestamp columns
    op.execute("ALTER TABLE reviews ALTER COLUMN created_at TYPE timestamp without time zone USING created_at AT TIME ZONE 'UTC'")
    op.execute("ALTER TABLE reviews ALTER COLUMN updated_at TYPE timestamp without time zone USING updated_at AT TIME ZONE 'UTC'")

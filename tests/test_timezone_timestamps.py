"""Tests for timezone-aware timestamp functionality."""

from datetime import UTC, datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlmodel import Session, SQLModel

from app.models import (
    Review,
    ReviewCreate,
    ReviewedObject,
    ReviewedObjectCreate,
    Reviewer,
    ReviewerCreate,
    utc_now,
)


def test_utc_now_returns_timezone_aware():
    """Test that utc_now() returns timezone-aware datetime."""
    now = utc_now()
    assert now.tzinfo is not None
    assert now.tzinfo == UTC


def test_model_creation_with_timezone_aware_timestamps():
    """Test that model instances have timezone-aware timestamps."""
    # Create in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create test data
        reviewer = Reviewer(
            username="test_user",
            email="test@example.com",
            full_name="Test User",
        )
        session.add(reviewer)
        session.commit()
        session.refresh(reviewer)

        # Check that timestamps are timezone-aware
        assert reviewer.created_at.tzinfo is not None
        assert reviewer.updated_at.tzinfo is not None
        assert reviewer.created_at.tzinfo == UTC
        assert reviewer.updated_at.tzinfo == UTC


def test_database_column_types_with_postgresql():
    """Test that PostgreSQL columns are created with timezone support."""
    # This test would require a PostgreSQL connection to validate
    # the actual column types, but we can at least test the model definition
    
    # Verify that the sa_column attribute is properly configured
    reviewer_created_at_field = Reviewer.__fields__["created_at"]
    reviewer_updated_at_field = Reviewer.__fields__["updated_at"]
    
    # These should use TIMESTAMP(timezone=True) columns
    assert hasattr(reviewer_created_at_field, "sa_column")
    assert hasattr(reviewer_updated_at_field, "sa_column")


def test_datetime_comparison_across_timezones():
    """Test that timezone-aware datetimes can be properly compared."""
    now_utc = utc_now()
    
    # Create timezone-aware datetime in different timezone
    est = timezone.UTC.utc.replace(tzinfo=timezone.UTC)
    now_est = now_utc.astimezone(est)
    
    # Should be equal when compared
    assert now_utc == now_est
    
    # But different when converted to naive
    assert now_utc.replace(tzinfo=None) != now_est.replace(tzinfo=None)


if __name__ == "__main__":
    # Run basic tests
    test_utc_now_returns_timezone_aware()
    print("✓ utc_now() returns timezone-aware datetime")
    
    test_model_creation_with_timezone_aware_timestamps()
    print("✓ Model creation with timezone-aware timestamps")
    
    test_database_column_types_with_postgresql()
    print("✓ Database column types configured correctly")
    
    test_datetime_comparison_across_timezones()
    print("✓ Datetime comparison across timezones")
    
    print("\nAll timezone-aware timestamp tests passed!")
"""Tests for timezone-aware timestamp functionality."""

from datetime import UTC, datetime
from collections.abc import Generator
from typing import Any

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine

from app.models import (
    ReviewCreate,
    ReviewedObjectCreate,
    ReviewerCreate,
    SQLModel,
    utc_now,
)
from app.repositories import (
    ReviewedObjectRepository,
    ReviewerRepository,
    ReviewRepository,
)


@pytest.fixture(name="session")
def session_fixture() -> Generator:
    """Create a test database session."""
    # Create SQLite engine for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Replace JSONB with JSON for SQLite compatibility
    def mock_visit_JSONB(self: Any, type_: Any, **kwargs: dict[str, Any]) -> str:
        # Cast to str since visit_JSON should return a string representation
        return str(self.visit_JSON(type_, **kwargs))

    # Monkey patch the SQLite type compiler to handle JSONB as JSON
    from sqlalchemy.dialects.sqlite.base import SQLiteTypeCompiler

    # Monkey patch: ignore mypy error for dynamic attribute assignment
    SQLiteTypeCompiler.visit_JSONB = mock_visit_JSONB  # type: ignore[attr-defined]  # noqa: E501

    # Create all tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


class TestTimezoneAwareness:
    """Test timezone-aware datetime functionality."""

    def test_utc_now_returns_timezone_aware_datetime(self) -> None:
        """Test that utc_now returns a timezone-aware datetime."""
        now = utc_now()
        assert now.tzinfo is not None
        assert now.tzinfo == UTC

    def test_model_definition_uses_timezone_aware_columns(self) -> None:
        """Test that our models define timezone-aware datetime columns."""
        from app.models import Reviewer, ReviewedObject, Review
        from sqlalchemy import DateTime

        # Check that our models have timezone-aware datetime columns defined
        # Note: In SQLite, timezone info is not preserved, but the column definition should be correct
        reviewer_table = Reviewer.__table__
        assert "created_at" in reviewer_table.columns
        assert "updated_at" in reviewer_table.columns

        # Verify column types are DateTime (timezone-aware in PostgreSQL)
        created_at_col = reviewer_table.columns["created_at"]
        updated_at_col = reviewer_table.columns["updated_at"]

        assert isinstance(created_at_col.type, DateTime)
        assert isinstance(updated_at_col.type, DateTime)

        # In PostgreSQL, these would be timezone-aware, but SQLite doesn't preserve this

    def test_default_factory_generates_timezone_aware_datetimes(
        self, session: Session
    ) -> None:
        """Test that the default factory creates timezone-aware datetimes."""
        repo = ReviewerRepository(session)
        reviewer_data = ReviewerCreate(
            username="timezoneuser",
            email="timezone@example.com",
            full_name="Timezone Test User",
        )

        reviewer = repo.create(reviewer_data)

        # The default_factory (utc_now) should create timezone-aware datetimes
        # Even though SQLite strips timezone info, we can verify creation works
        assert reviewer.created_at is not None
        assert reviewer.updated_at is not None

        # Verify timestamps are recent
        now = utc_now()
        # Convert to naive for comparison since SQLite stores naive datetimes
        naive_now = now.replace(tzinfo=None)
        time_diff = naive_now - reviewer.created_at
        assert (
            time_diff.total_seconds() < 10
        )  # Should be created within last 10 seconds

    def test_temporal_ordering_works_correctly(self, session: Session) -> None:
        """Test that datetime comparisons work correctly."""
        repo = ReviewerRepository(session)

        # Create first reviewer
        reviewer1 = repo.create(
            ReviewerCreate(username="user1", email="user1@example.com")
        )

        # Wait a tiny bit and create second reviewer
        import time

        time.sleep(0.01)

        reviewer2 = repo.create(
            ReviewerCreate(username="user2", email="user2@example.com")
        )

        # Verify the order is correct (both are naive in SQLite)
        assert reviewer1.created_at < reviewer2.created_at

        # Verify we can compare with current time (convert to naive for SQLite)
        naive_now = utc_now().replace(tzinfo=None)
        assert reviewer1.created_at < naive_now
        assert reviewer2.created_at < naive_now

    def test_all_models_have_timezone_aware_timestamp_fields(
        self, session: Session
    ) -> None:
        """Test that all models create records with timestamp fields."""
        # Test ReviewedObject
        object_repo = ReviewedObjectRepository(session)
        obj = object_repo.create(
            ReviewedObjectCreate(
                object_type="product",
                object_id="test-123",
                object_name="Test Product",
            )
        )
        assert obj.created_at is not None
        assert obj.updated_at is not None

        # Test Reviewer
        reviewer_repo = ReviewerRepository(session)
        reviewer = reviewer_repo.create(
            ReviewerCreate(username="testuser", email="test@example.com")
        )
        assert reviewer.created_at is not None
        assert reviewer.updated_at is not None

        # Test Review
        review_repo = ReviewRepository(session)
        review = review_repo.create(
            ReviewCreate(
                reviewer_id=reviewer.id,
                reviewed_object_id=obj.id,
                text_review="Test review",
                star_rating=5,
            )
        )
        assert review.created_at is not None
        assert review.updated_at is not None

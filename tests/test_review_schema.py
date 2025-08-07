"""Tests for the review management database schema and repository."""

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
    def mock_visit_JSONB(
        self: Any, type_: Any, **kwargs: dict[str, Any]
    ) -> str:
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


class TestReviewerRepository:
    """Test the ReviewerRepository."""

    def test_create_reviewer(self, session: Session) -> None:
        """Test creating a new reviewer."""
        repo = ReviewerRepository(session)
        reviewer_data = ReviewerCreate(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
        )

        reviewer = repo.create(reviewer_data)

        assert reviewer.id is not None
        assert reviewer.username == "testuser"
        assert reviewer.email == "test@example.com"
        assert reviewer.full_name == "Test User"
        assert reviewer.created_at is not None
        assert reviewer.updated_at is not None

    def test_get_reviewer_by_id(self, session: Session) -> None:
        """Test getting a reviewer by ID."""
        repo = ReviewerRepository(session)
        reviewer_data = ReviewerCreate(
            username="testuser", email="test@example.com"
        )

        created_reviewer = repo.create(reviewer_data)
        retrieved_reviewer = repo.get_by_id(created_reviewer.id)

        assert retrieved_reviewer is not None
        assert retrieved_reviewer.id == created_reviewer.id
        assert retrieved_reviewer.username == "testuser"

    def test_get_reviewer_by_username(self, session: Session) -> None:
        """Test getting a reviewer by username."""
        repo = ReviewerRepository(session)
        reviewer_data = ReviewerCreate(
            username="testuser", email="test@example.com"
        )

        repo.create(reviewer_data)
        retrieved_reviewer = repo.get_by_username("testuser")

        assert retrieved_reviewer is not None
        assert retrieved_reviewer.username == "testuser"

    def test_unique_username_constraint(self, session: Session) -> None:
        """Test that username must be unique."""
        repo = ReviewerRepository(session)
        reviewer_data1 = ReviewerCreate(
            username="testuser", email="test1@example.com"
        )
        reviewer_data2 = ReviewerCreate(
            username="testuser", email="test2@example.com"
        )

        repo.create(reviewer_data1)

        with pytest.raises(ValueError, match="Reviewer creation failed"):
            repo.create(reviewer_data2)


class TestReviewedObjectRepository:
    """Test the ReviewedObjectRepository."""

    def test_create_reviewed_object(self, session: Session) -> None:
        """Test creating a new reviewed object."""
        repo = ReviewedObjectRepository(session)
        object_data = ReviewedObjectCreate(
            object_type="product",
            object_id="prod123",
            object_name="Test Product",
            object_description="A test product",
        )

        reviewed_object = repo.create(object_data)

        assert reviewed_object.id is not None
        assert reviewed_object.object_type == "product"
        assert reviewed_object.object_id == "prod123"
        assert reviewed_object.object_name == "Test Product"
        assert reviewed_object.object_description == "A test product"

    def test_get_by_type_and_id(self, session: Session) -> None:
        """Test getting object by type and external ID."""
        repo = ReviewedObjectRepository(session)
        object_data = ReviewedObjectCreate(
            object_type="movie", object_id="movie456", object_name="Test Movie"
        )

        repo.create(object_data)
        retrieved_object = repo.get_by_type_and_id("movie", "movie456")

        assert retrieved_object is not None
        assert retrieved_object.object_type == "movie"
        assert retrieved_object.object_id == "movie456"

    def test_unique_type_id_constraint(self, session: Session) -> None:
        """Test that object_type + object_id must be unique."""
        repo = ReviewedObjectRepository(session)
        object_data1 = ReviewedObjectCreate(
            object_type="product", object_id="prod123", object_name="Product 1"
        )
        object_data2 = ReviewedObjectCreate(
            object_type="product", object_id="prod123", object_name="Product 2"
        )

        repo.create(object_data1)

        with pytest.raises(
            ValueError, match="Reviewed object creation failed"
        ):
            repo.create(object_data2)


class TestReviewRepository:
    """Test the ReviewRepository."""

    def test_create_review(self, session: Session) -> None:
        """Test creating a new review."""
        # Create test data
        reviewer_repo = ReviewerRepository(session)
        object_repo = ReviewedObjectRepository(session)
        review_repo = ReviewRepository(session)

        reviewer = reviewer_repo.create(
            ReviewerCreate(username="reviewer1", email="reviewer1@example.com")
        )

        reviewed_object = object_repo.create(
            ReviewedObjectCreate(
                object_type="movie",
                object_id="movie123",
                object_name="Great Movie",
            )
        )

        review_data = ReviewCreate(
            reviewer_id=reviewer.id,
            reviewed_object_id=reviewed_object.id,
            text_review="This is a great movie!",
            star_rating=5,
            thumbs_rating="up",
        )

        review = review_repo.create(review_data)

        assert review.id is not None
        assert review.reviewer_id == reviewer.id
        assert review.reviewed_object_id == reviewed_object.id
        assert review.text_review == "This is a great movie!"
        assert review.star_rating == 5
        assert review.thumbs_rating == "up"

    def test_review_with_only_text(self, session: Session) -> None:
        """Test creating a review with only text."""
        reviewer_repo = ReviewerRepository(session)
        object_repo = ReviewedObjectRepository(session)
        review_repo = ReviewRepository(session)

        reviewer = reviewer_repo.create(
            ReviewerCreate(username="reviewer2", email="reviewer2@example.com")
        )

        reviewed_object = object_repo.create(
            ReviewedObjectCreate(
                object_type="book",
                object_id="book456",
                object_name="Good Book",
            )
        )

        review_data = ReviewCreate(
            reviewer_id=reviewer.id,
            reviewed_object_id=reviewed_object.id,
            text_review="Interesting read.",
        )

        review = review_repo.create(review_data)

        assert review.text_review == "Interesting read."
        assert review.star_rating is None
        assert review.thumbs_rating is None

    def test_review_with_only_star_rating(self, session: Session) -> None:
        """Test creating a review with only star rating."""
        reviewer_repo = ReviewerRepository(session)
        object_repo = ReviewedObjectRepository(session)
        review_repo = ReviewRepository(session)

        reviewer = reviewer_repo.create(
            ReviewerCreate(username="reviewer3", email="reviewer3@example.com")
        )

        reviewed_object = object_repo.create(
            ReviewedObjectCreate(
                object_type="restaurant",
                object_id="rest789",
                object_name="Good Restaurant",
            )
        )

        review_data = ReviewCreate(
            reviewer_id=reviewer.id,
            reviewed_object_id=reviewed_object.id,
            star_rating=4,
        )

        review = review_repo.create(review_data)

        assert review.star_rating == 4
        assert review.text_review is None
        assert review.thumbs_rating is None

    def test_unique_reviewer_object_constraint(self, session: Session) -> None:
        """Test that one reviewer can only review an object once."""
        reviewer_repo = ReviewerRepository(session)
        object_repo = ReviewedObjectRepository(session)
        review_repo = ReviewRepository(session)

        reviewer = reviewer_repo.create(
            ReviewerCreate(username="reviewer4", email="reviewer4@example.com")
        )

        reviewed_object = object_repo.create(
            ReviewedObjectCreate(
                object_type="event",
                object_id="event101",
                object_name="Concert",
            )
        )

        review_data1 = ReviewCreate(
            reviewer_id=reviewer.id,
            reviewed_object_id=reviewed_object.id,
            text_review="Great concert!",
        )

        review_data2 = ReviewCreate(
            reviewer_id=reviewer.id,
            reviewed_object_id=reviewed_object.id,
            text_review="Actually, it was just okay.",
        )

        review_repo.create(review_data1)

        with pytest.raises(ValueError, match="Review creation failed"):
            review_repo.create(review_data2)

    def test_get_reviews_by_object(self, session: Session) -> None:
        """Test getting all reviews for an object."""
        reviewer_repo = ReviewerRepository(session)
        object_repo = ReviewedObjectRepository(session)
        review_repo = ReviewRepository(session)

        # Create two reviewers
        reviewer1 = reviewer_repo.create(
            ReviewerCreate(username="reviewer5", email="reviewer5@example.com")
        )
        reviewer2 = reviewer_repo.create(
            ReviewerCreate(username="reviewer6", email="reviewer6@example.com")
        )

        # Create an object
        reviewed_object = object_repo.create(
            ReviewedObjectCreate(
                object_type="store",
                object_id="store202",
                object_name="Local Store",
            )
        )

        # Create reviews from both reviewers
        review_repo.create(
            ReviewCreate(
                reviewer_id=reviewer1.id,
                reviewed_object_id=reviewed_object.id,
                star_rating=5,
            )
        )
        review_repo.create(
            ReviewCreate(
                reviewer_id=reviewer2.id,
                reviewed_object_id=reviewed_object.id,
                star_rating=3,
            )
        )

        reviews = review_repo.get_by_object(reviewed_object.id)

        assert len(reviews) == 2
        star_ratings = [review.star_rating for review in reviews]
        assert 5 in star_ratings
        assert 3 in star_ratings

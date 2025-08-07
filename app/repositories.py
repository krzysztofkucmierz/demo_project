"""Repository pattern implementation for database access."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from .models import (
    Review,
    ReviewCreate,
    ReviewedObject,
    ReviewedObjectCreate,
    ReviewedObjectUpdate,
    Reviewer,
    ReviewerCreate,
    ReviewerUpdate,
    ReviewUpdate,
)


class ReviewerRepository:
    """Repository for reviewer database operations."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, reviewer_data: ReviewerCreate) -> Reviewer:
        """Create a new reviewer."""
        reviewer = Reviewer.model_validate(reviewer_data)
        self.session.add(reviewer)
        try:
            self.session.commit()
            self.session.refresh(reviewer)
            return reviewer
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Reviewer creation failed: {e}") from e

    def get_by_id(self, reviewer_id: UUID) -> Reviewer | None:
        """Get reviewer by ID."""
        return self.session.get(Reviewer, reviewer_id)

    def get_by_username(self, username: str) -> Reviewer | None:
        """Get reviewer by username."""
        statement = select(Reviewer).where(Reviewer.username == username)
        return self.session.exec(statement).first()

    def get_by_email(self, email: str) -> Reviewer | None:
        """Get reviewer by email."""
        statement = select(Reviewer).where(Reviewer.email == email)
        return self.session.exec(statement).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Reviewer]:
        """Get all reviewers with pagination."""
        statement = select(Reviewer).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(
        self, reviewer_id: UUID, reviewer_data: ReviewerUpdate
    ) -> Reviewer | None:
        """Update reviewer."""
        reviewer = self.session.get(Reviewer, reviewer_id)
        if not reviewer:
            return None

        reviewer_update_data = reviewer_data.model_dump(exclude_unset=True)
        for field, value in reviewer_update_data.items():
            setattr(reviewer, field, value)

        try:
            self.session.add(reviewer)
            self.session.commit()
            self.session.refresh(reviewer)
            return reviewer
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Reviewer update failed: {e}") from e

    def delete(self, reviewer_id: UUID) -> bool:
        """Delete reviewer."""
        reviewer = self.session.get(Reviewer, reviewer_id)
        if not reviewer:
            return False

        self.session.delete(reviewer)
        self.session.commit()
        return True


class ReviewedObjectRepository:
    """Repository for reviewed object database operations."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, object_data: ReviewedObjectCreate) -> ReviewedObject:
        """Create a new reviewed object."""
        reviewed_object = ReviewedObject.model_validate(object_data)
        self.session.add(reviewed_object)
        try:
            self.session.commit()
            self.session.refresh(reviewed_object)
            return reviewed_object
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Reviewed object creation failed: {e}") from e

    def get_by_id(self, object_id: UUID) -> ReviewedObject | None:
        """Get reviewed object by ID."""
        return self.session.get(ReviewedObject, object_id)

    def get_by_type_and_id(
        self, object_type: str, object_id: str
    ) -> ReviewedObject | None:
        """Get reviewed object by type and external ID."""
        statement = select(ReviewedObject).where(
            ReviewedObject.object_type == object_type,
            ReviewedObject.object_id == object_id,
        )
        return self.session.exec(statement).first()

    def get_by_type(
        self, object_type: str, skip: int = 0, limit: int = 100
    ) -> Sequence[ReviewedObject]:
        """Get reviewed objects by type with pagination."""
        statement = (
            select(ReviewedObject)
            .where(ReviewedObject.object_type == object_type)
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> Sequence[ReviewedObject]:
        """Get all reviewed objects with pagination."""
        statement = select(ReviewedObject).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(
        self, object_id: UUID, object_data: ReviewedObjectUpdate
    ) -> ReviewedObject | None:
        """Update reviewed object."""
        reviewed_object = self.session.get(ReviewedObject, object_id)
        if not reviewed_object:
            return None

        object_update_data = object_data.model_dump(exclude_unset=True)
        for field, value in object_update_data.items():
            setattr(reviewed_object, field, value)

        try:
            self.session.add(reviewed_object)
            self.session.commit()
            self.session.refresh(reviewed_object)
            return reviewed_object
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Reviewed object update failed: {e}") from e

    def delete(self, object_id: UUID) -> bool:
        """Delete reviewed object."""
        reviewed_object = self.session.get(ReviewedObject, object_id)
        if not reviewed_object:
            return False

        self.session.delete(reviewed_object)
        self.session.commit()
        return True


class ReviewRepository:
    """Repository for review database operations."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, review_data: ReviewCreate) -> Review:
        """Create a new review."""
        review = Review.model_validate(review_data)
        self.session.add(review)
        try:
            self.session.commit()
            self.session.refresh(review)
            return review
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Review creation failed: {e}") from e

    def get_by_id(self, review_id: UUID) -> Review | None:
        """Get review by ID."""
        return self.session.get(Review, review_id)

    def get_by_reviewer(
        self, reviewer_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[Review]:
        """Get reviews by reviewer with pagination."""
        statement = (
            select(Review)
            .where(Review.reviewer_id == reviewer_id)
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def get_by_object(
        self, object_id: UUID, skip: int = 0, limit: int = 100
    ) -> Sequence[Review]:
        """Get reviews by reviewed object with pagination."""
        statement = (
            select(Review)
            .where(Review.reviewed_object_id == object_id)
            .offset(skip)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def get_by_reviewer_and_object(
        self, reviewer_id: UUID, object_id: UUID
    ) -> Review | None:
        """Get review by reviewer and object (should be unique)."""
        statement = select(Review).where(
            Review.reviewer_id == reviewer_id,
            Review.reviewed_object_id == object_id,
        )
        return self.session.exec(statement).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Review]:
        """Get all reviews with pagination."""
        statement = select(Review).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(
        self, review_id: UUID, review_data: ReviewUpdate
    ) -> Review | None:
        """Update review."""
        review = self.session.get(Review, review_id)
        if not review:
            return None

        review_update_data = review_data.model_dump(exclude_unset=True)
        for field, value in review_update_data.items():
            setattr(review, field, value)

        try:
            self.session.add(review)
            self.session.commit()
            self.session.refresh(review)
            return review
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Review update failed: {e}") from e

    def delete(self, review_id: UUID) -> bool:
        """Delete review."""
        review = self.session.get(Review, review_id)
        if not review:
            return False

        self.session.delete(review)
        self.session.commit()
        return True

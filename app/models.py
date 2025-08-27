"""Database models for the review management module."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, Relationship, SQLModel


def utc_now() -> datetime:
    """Get current UTC datetime.

    Replacement for deprecated datetime.utcnow().
    """
    return datetime.now(UTC)


class ReviewerBase(SQLModel):
    """Base model for reviewer data."""

    username: str = Field(max_length=50, unique=True, index=True)
    email: str = Field(max_length=255, unique=True, index=True)
    full_name: str | None = Field(default=None, max_length=255)


class Reviewer(ReviewerBase, table=True):
    """Reviewer model representing users who can submit reviews."""

    __tablename__ = "reviewers"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")),
    )

    # Relationships
    reviews: list["Review"] = Relationship(back_populates="reviewer")


class ReviewerCreate(ReviewerBase):
    """Model for creating a new reviewer."""

    pass


class ReviewerRead(ReviewerBase):
    """Model for reading reviewer data."""

    id: UUID
    created_at: datetime
    updated_at: datetime


class ReviewerUpdate(SQLModel):
    """Model for updating reviewer data."""

    username: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=255)
    full_name: str | None = Field(default=None, max_length=255)


class ReviewedObjectBase(SQLModel):
    """Base model for reviewed object data."""

    object_type: str = Field(max_length=50, index=True)
    object_id: str = Field(max_length=255)
    object_name: str = Field(max_length=255)
    object_description: str | None = Field(default=None)
    object_metadata: dict | None = Field(default=None, sa_column=Column(JSONB))


class ReviewedObject(ReviewedObjectBase, table=True):
    """Model representing objects that can be reviewed."""

    __tablename__ = "reviewed_objects"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")),
    )

    # Relationships
    reviews: list["Review"] = Relationship(back_populates="reviewed_object")

    # Constraints
    __table_args__ = (
        UniqueConstraint("object_type", "object_id", name="uq_object_type_id"),
    )


class ReviewedObjectCreate(ReviewedObjectBase):
    """Model for creating a new reviewed object."""

    pass


class ReviewedObjectRead(ReviewedObjectBase):
    """Model for reading reviewed object data."""

    id: UUID
    created_at: datetime
    updated_at: datetime


class ReviewedObjectUpdate(SQLModel):
    """Model for updating reviewed object data."""

    object_type: str | None = Field(default=None, max_length=50)
    object_id: str | None = Field(default=None, max_length=255)
    object_name: str | None = Field(default=None, max_length=255)
    object_description: str | None = Field(default=None)
    object_metadata: dict | None = Field(default=None, sa_column=Column(JSONB))


class ReviewBase(SQLModel):
    """Base model for review data."""

    text_review: str | None = Field(default=None)
    star_rating: int | None = Field(default=None, ge=0, le=5)
    thumbs_rating: str | None = Field(default=None, max_length=10)


class Review(ReviewBase, table=True):
    """Model representing reviews submitted by users."""

    __tablename__ = "reviews"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    reviewer_id: UUID = Field(foreign_key="reviewers.id")
    reviewed_object_id: UUID = Field(foreign_key="reviewed_objects.id")
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")),
    )

    # Relationships
    reviewer: Reviewer = Relationship(back_populates="reviews")
    reviewed_object: ReviewedObject = Relationship(back_populates="reviews")

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "star_rating >= 0 AND star_rating <= 5",
            name="check_star_rating_range",
        ),
        CheckConstraint(
            "thumbs_rating IN ('up', 'down') OR thumbs_rating IS NULL",
            name="check_thumbs_rating_values",
        ),
        CheckConstraint(
            (
                "text_review IS NOT NULL OR star_rating IS NOT NULL "
                "OR thumbs_rating IS NOT NULL"
            ),
            name="check_review_content_exists",
        ),
        UniqueConstraint(
            "reviewer_id", "reviewed_object_id", name="uq_reviewer_object"
        ),
    )


class ReviewCreate(ReviewBase):
    """Model for creating a new review."""

    reviewer_id: UUID
    reviewed_object_id: UUID


class ReviewRead(ReviewBase):
    """Model for reading review data."""

    id: UUID
    reviewer_id: UUID
    reviewed_object_id: UUID
    created_at: datetime
    updated_at: datetime


class ReviewUpdate(SQLModel):
    """Model for updating review data."""

    text_review: str | None = Field(default=None)
    star_rating: int | None = Field(default=None, ge=0, le=5)
    thumbs_rating: str | None = Field(default=None, max_length=10)


# Review statistics view model (read-only)
class ReviewStatistics(SQLModel):
    """Model for review statistics per object."""

    object_id: UUID
    object_type: str
    object_name: str
    total_reviews: int
    average_rating: float | None
    thumbs_up_count: int
    thumbs_down_count: int

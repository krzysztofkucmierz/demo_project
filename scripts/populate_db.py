#!/usr/bin/env python3
"""
Database population script for demo_project.

Populates the database with realistic test data:
- 50 reviewers with real-looking names
- 50 restaurants with varied metadata
- 400 reviews with mixed rating types and realistic distribution

Usage:
    uv run python scripts/populate_db.py
"""

import random

from sqlmodel import Session

from app.database import engine
from app.models import (
    Review,
    ReviewCreate,
    ReviewedObject,
    ReviewedObjectCreate,
    Reviewer,
    ReviewerCreate,
)
from app.repositories import (
    ReviewedObjectRepository,
    ReviewerRepository,
    ReviewRepository,
)

# Sample data for generating realistic content
FIRST_NAMES = [
    "James",
    "Mary",
    "John",
    "Patricia",
    "Robert",
    "Jennifer",
    "Michael",
    "Linda",
    "William",
    "Elizabeth",
    "David",
    "Barbara",
    "Richard",
    "Susan",
    "Joseph",
    "Jessica",
    "Thomas",
    "Sarah",
    "Christopher",
    "Karen",
    "Charles",
    "Nancy",
    "Daniel",
    "Lisa",
    "Matthew",
    "Betty",
    "Anthony",
    "Helen",
    "Mark",
    "Sandra",
    "Donald",
    "Donna",
    "Steven",
    "Carol",
    "Paul",
    "Ruth",
    "Andrew",
    "Sharon",
    "Joshua",
    "Michelle",
    "Kenneth",
    "Laura",
    "Kevin",
    "Emily",
    "Brian",
    "Kimberly",
    "George",
    "Deborah",
    "Timothy",
    "Dorothy",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Perez",
    "Thompson",
    "White",
    "Harris",
    "Sanchez",
    "Clark",
    "Ramirez",
    "Lewis",
    "Robinson",
    "Walker",
    "Young",
    "Allen",
    "King",
    "Wright",
    "Scott",
    "Torres",
    "Nguyen",
    "Hill",
    "Flores",
    "Green",
    "Adams",
    "Nelson",
    "Baker",
    "Hall",
    "Rivera",
    "Campbell",
    "Mitchell",
    "Carter",
    "Roberts",
]

RESTAURANT_NAMES = [
    "The Golden Spoon",
    "Mama's Kitchen",
    "Blue Ocean Bistro",
    "Sunset Grill",
    "The Cozy Corner",
    "Fire & Stone",
    "Garden Fresh Cafe",
    "The Rustic Table",
    "Urban Eats",
    "Seaside Tavern",
    "The Green Olive",
    "Smokehouse BBQ",
    "Bella Vista",
    "The Hungry Bear",
    "Crispy Chicken Co",
    "Ocean View Restaurant",
    "The Local Diner",
    "Spice Route",
    "The Morning Glory",
    "Riverbank Grill",
    "The Corner Cafe",
    "Mountain View Eatery",
    "The Wine Bar",
    "Fresh & Fast",
    "The Pizza Place",
    "Grandma's Recipes",
    "The Steakhouse",
    "Fusion Kitchen",
    "The Coffee Shop",
    "Harbor Lights",
    "The Breakfast Nook",
    "Zen Garden",
    "The Burger Joint",
    "Taste of Home",
    "The Sandwich Shop",
    "Moonlight Diner",
    "The Pasta House",
    "Healthy Bites",
    "The Food Truck",
    "Downtown Delights",
    "The Ice Cream Parlor",
    "Lucky Dragon",
    "The Fish Market",
    "Corner Bakery",
    "The Taco Stand",
    "Sweet Dreams Desserts",
    "The Beer Garden",
    "City Lights Cafe",
    "The Soup Kitchen",
    "Rooftop Restaurant",
]

CUISINES = [
    "American",
    "Italian",
    "Mexican",
    "Chinese",
    "Japanese",
    "Thai",
    "Indian",
    "French",
    "Mediterranean",
    "Greek",
    "Spanish",
    "Korean",
    "Vietnamese",
    "Brazilian",
    "German",
    "Middle Eastern",
    "Seafood",
    "Steakhouse",
    "Pizza",
    "Burger",
    "Fast Food",
    "Cafe",
    "Bakery",
    "BBQ",
    "Vegetarian",
]

NEIGHBORHOODS = [
    "Downtown",
    "Uptown",
    "Midtown",
    "Old Town",
    "Riverside",
    "Hillcrest",
    "Westside",
    "Eastside",
    "Central",
    "Northside",
    "Southside",
    "Waterfront",
    "Historic District",
    "Arts Quarter",
    "Business District",
]

REVIEW_TEXTS = {
    5: [
        "Absolutely amazing! Best meal I've had in years.",
        "Outstanding service and incredible food quality.",
        "Perfect in every way. Will definitely be back!",
        "Exceeded all expectations. Highly recommend!",
        "Fantastic atmosphere and delicious food.",
        "Five stars well deserved. Everything was perfect.",
        "Amazing experience from start to finish.",
        "The best restaurant in town, hands down!",
    ],
    4: [
        "Really good food and great service.",
        "Very enjoyable meal with minor room for improvement.",
        "Solid choice, would recommend to friends.",
        "Good quality and reasonable prices.",
        "Nice atmosphere and tasty dishes.",
        "Above average experience overall.",
        "Good food, friendly staff.",
        "Satisfying meal with good portion sizes.",
    ],
    3: [
        "Decent food, nothing special but acceptable.",
        "Average experience, met expectations.",
        "It was okay, might try again.",
        "Fair value for money.",
        "Not bad, but I've had better.",
        "Standard quality for this type of restaurant.",
        "Acceptable but room for improvement.",
        "Middle of the road dining experience.",
    ],
    2: [
        "Below expectations, service was slow.",
        "Food was cold when it arrived.",
        "Not worth the price we paid.",
        "Several issues with our order.",
        "Disappointing experience overall.",
        "Food quality needs improvement.",
        "Service was lacking attention.",
        "Won't be returning anytime soon.",
    ],
    1: [
        "Terrible experience, would not recommend.",
        "Poor service and bad food quality.",
        "Complete waste of time and money.",
        "Worst meal I've had in a long time.",
        "Everything went wrong during our visit.",
        "Unacceptable quality for the price.",
        "Very disappointing on all fronts.",
        "Save your money and go elsewhere.",
    ],
}


def clear_existing_data(session: Session) -> None:
    """Clear all existing data from the database."""
    print("🗑️  Clearing existing data...")

    # Delete in order to respect foreign key constraints using proper SQLAlchemy
    from sqlalchemy import text

    session.execute(text("DELETE FROM reviews"))
    session.execute(text("DELETE FROM reviewed_objects"))
    session.execute(text("DELETE FROM reviewers"))

    session.commit()
    print("✅ Existing data cleared")

def create_reviewers(session: Session, count: int = 50) -> list[Reviewer]:
    """Create realistic reviewer data."""
    print(f"👥 Creating {count} reviewers...")

    reviewer_repo = ReviewerRepository(session)
    reviewers = []

    for _ in range(count):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name}"

        # Create realistic username and email
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
        email = f"{username}@example.com"

        reviewer_data = ReviewerCreate(
            username=username, email=email, full_name=full_name
        )

        reviewer = reviewer_repo.create(reviewer_data)
        reviewers.append(reviewer)

    print(f"✅ Created {len(reviewers)} reviewers")
    return reviewers


def create_restaurants(session: Session, count: int = 50) -> list[ReviewedObject]:
    """Create realistic restaurant data."""
    print(f"🍽️  Creating {count} restaurants...")

    object_repo = ReviewedObjectRepository(session)
    restaurants = []

    for i in range(count):
        name = random.choice(RESTAURANT_NAMES)
        cuisine = random.choice(CUISINES)
        neighborhood = random.choice(NEIGHBORHOODS)

        # Generate realistic metadata
        metadata = {
            "cuisine": cuisine,
            "neighborhood": neighborhood,
            "price_range": random.choice(["$", "$$", "$$$", "$$$$"]),
            "phone": f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'First', 'Second'])} St",
            "has_parking": random.choice([True, False]),
            "outdoor_seating": random.choice([True, False]),
            "accepts_reservations": random.choice([True, False]),
            "delivery_available": random.choice([True, False]),
        }

        restaurant_data = ReviewedObjectCreate(
            object_type="restaurant",
            object_id=f"rest_{i+1:03d}",
            object_name=name,
            object_description=f"A {cuisine.lower()} restaurant in {neighborhood}",
            object_metadata=metadata,
        )

        restaurant = object_repo.create(restaurant_data)
        restaurants.append(restaurant)

    print(f"✅ Created {len(restaurants)} restaurants")
    return restaurants


def create_reviews(
    session: Session,
    reviewers: list[Reviewer],
    restaurants: list[ReviewedObject],
    count: int = 400,
) -> list[Review]:
    """Create realistic review data with varied distribution."""
    print(f"⭐ Creating {count} reviews...")

    review_repo = ReviewRepository(session)
    reviews: list[Review] = []

    # Create weighted distribution for star ratings (more 4-5 stars, fewer 1-2)
    star_weights = [5, 10, 20, 35, 30]  # 1-star, 2-star, 3-star, 4-star, 5-star
    star_distribution = []
    for rating, weight in enumerate(star_weights, 1):
        star_distribution.extend([rating] * weight)

    # Track reviewer-restaurant combinations to avoid duplicates
    used_combinations = set()

    attempts = 0
    max_attempts = count * 3  # Prevent infinite loop

    while len(reviews) < count and attempts < max_attempts:
        attempts += 1

        reviewer = random.choice(reviewers)
        restaurant = random.choice(restaurants)

        # Check if this combination already exists
        combo_key = (reviewer.id, restaurant.id)
        if combo_key in used_combinations:
            continue

        used_combinations.add(combo_key)

        # Determine review type (40% text only, 30% star only, 20% thumbs only, 10% mixed)
        review_type = random.choices(
            ["text_star", "text_only", "star_only", "thumbs_only", "mixed"],
            weights=[25, 25, 25, 15, 10],
        )[0]

        # Generate review content based on type
        text_review = None
        star_rating = None
        thumbs_rating = None

        if review_type in ["text_star", "text_only", "mixed"]:
            # Generate star rating first to match text sentiment
            if review_type != "text_only":
                star_rating = random.choice(star_distribution)
            else:
                # For text-only, still pick a rating to generate appropriate text
                star_rating = random.choice(star_distribution)

            text_review = random.choice(REVIEW_TEXTS[star_rating])

            # Reset star_rating to None for text_only
            if review_type == "text_only":
                star_rating = None

        if review_type in ["star_only", "text_star"]:
            if star_rating is None:
                star_rating = random.choice(star_distribution)

        if review_type in ["thumbs_only", "mixed"]:
            # Thumbs rating based on sentiment
            if star_rating is not None:
                thumbs_rating = "up" if star_rating >= 4 else "down"
            else:
                thumbs_rating = random.choice(["up", "down"])

        # For mixed reviews, sometimes add thumbs that might contradict
        if review_type == "mixed" and random.random() < 0.1:
            thumbs_rating = random.choice(["up", "down"])

        try:
            review_data = ReviewCreate(
                reviewer_id=reviewer.id,
                reviewed_object_id=restaurant.id,
                text_review=text_review,
                star_rating=star_rating,
                thumbs_rating=thumbs_rating,
            )

            review = review_repo.create(review_data)
            reviews.append(review)

        except Exception as e:
            print(f"⚠️  Failed to create review: {e}")
            continue

    print(f"✅ Created {len(reviews)} reviews")
    return reviews


def print_summary(
    reviewers: list[Reviewer],
    restaurants: list[ReviewedObject],
    reviews: list[Review],
) -> None:
    """Print summary statistics of the created data."""
    print("\n" + "=" * 50)
    print("📊 DATABASE POPULATION SUMMARY")
    print("=" * 50)
    print(f"👥 Reviewers created: {len(reviewers)}")
    print(f"🍽️  Restaurants created: {len(restaurants)}")
    print(f"⭐ Reviews created: {len(reviews)}")

    # Review type breakdown
    text_only = sum(
        1
        for r in reviews
        if r.text_review and not r.star_rating and not r.thumbs_rating
    )
    star_only = sum(
        1
        for r in reviews
        if r.star_rating and not r.text_review and not r.thumbs_rating
    )
    thumbs_only = sum(
        1
        for r in reviews
        if r.thumbs_rating and not r.text_review and not r.star_rating
    )
    mixed = len(reviews) - text_only - star_only - thumbs_only

    print("\n📝 Review breakdown:")
    print(f"  Text only: {text_only}")
    print(f"  Star only: {star_only}")
    print(f"  Thumbs only: {thumbs_only}")
    print(f"  Mixed: {mixed}")

    # Star rating distribution
    star_counts = {}
    for i in range(1, 6):
        count = sum(1 for r in reviews if r.star_rating == i)
        star_counts[i] = count
        if count > 0:
            print(f"  {i} stars: {count}")

    # Thumbs distribution
    thumbs_up = sum(1 for r in reviews if r.thumbs_rating == "up")
    thumbs_down = sum(1 for r in reviews if r.thumbs_rating == "down")
    if thumbs_up > 0 or thumbs_down > 0:
        print("\n👍 Thumbs breakdown:")
        print(f"  Thumbs up: {thumbs_up}")
        print(f"  Thumbs down: {thumbs_down}")

    print("\n✅ Database population completed successfully!")
    print("=" * 50)


def main() -> None:
    """Main function to populate the database."""
    print("🚀 Starting database population...")
    print("📍 Target: 50 reviewers, 50 restaurants, 400 reviews")

    try:
        with Session(engine) as session:
            # Clear existing data
            clear_existing_data(session)

            # Create test data
            reviewers = create_reviewers(session, 50)
            restaurants = create_restaurants(session, 50)
            reviews = create_reviews(session, reviewers, restaurants, 400)

            # Print summary
            print_summary(reviewers, restaurants, reviews)

    except Exception as e:
        print(f"❌ Error during database population: {e}")
        raise


if __name__ == "__main__":
    main()

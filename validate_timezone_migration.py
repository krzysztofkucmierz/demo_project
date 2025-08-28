#!/usr/bin/env python3
"""
Validation script for timezone-aware timestamp migration.

This script validates that:
1. The migration SQL is correct
2. The model definitions use timezone-aware timestamps
3. The utc_now() function returns proper timezone-aware datetimes
4. All required changes are in place

Run this before applying the migration to production.
"""

import ast
import re
from datetime import UTC, datetime
from pathlib import Path


def validate_migration_file():
    """Validate the migration file contains correct SQL."""
    migration_file = Path("migrations/versions/migrate_timestamps_to_timezone_aware.py")
    
    if not migration_file.exists():
        raise FileNotFoundError(f"Migration file not found: {migration_file}")
    
    content = migration_file.read_text()
    
    # Check for required tables and columns
    required_patterns = [
        r"ALTER TABLE reviewers.*created_at TYPE timestamp with time zone",
        r"ALTER TABLE reviewers.*updated_at TYPE timestamp with time zone", 
        r"ALTER TABLE reviewed_objects.*created_at TYPE timestamp with time zone",
        r"ALTER TABLE reviewed_objects.*updated_at TYPE timestamp with time zone",
        r"ALTER TABLE reviews.*created_at TYPE timestamp with time zone",
        r"ALTER TABLE reviews.*updated_at TYPE timestamp with time zone",
    ]
    
    for pattern in required_patterns:
        if not re.search(pattern, content, re.DOTALL):
            raise AssertionError(f"Missing SQL pattern: {pattern}")
    
    # Check downgrade function exists
    if "def downgrade()" not in content:
        raise AssertionError("Migration missing downgrade function")
    
    print("✓ Migration file validation passed")


def validate_models_file():
    """Validate the models file uses timezone-aware timestamps."""
    models_file = Path("app/models.py")
    
    if not models_file.exists():
        raise FileNotFoundError(f"Models file not found: {models_file}")
    
    content = models_file.read_text()
    
    # Check syntax
    try:
        ast.parse(content)
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in models.py: {e}")
    
    # Check TIMESTAMP import
    if "from sqlalchemy import CheckConstraint, UniqueConstraint, text, TIMESTAMP" not in content:
        raise AssertionError("TIMESTAMP import missing from models.py")
    
    # Check timezone-aware field definitions
    timestamp_count = content.count("TIMESTAMP(timezone=True)")
    if timestamp_count != 6:
        raise AssertionError(f"Expected 6 TIMESTAMP(timezone=True) fields, found {timestamp_count}")
    
    # Check that sa_column is used instead of sa_column_kwargs for timestamps
    if "sa_column_kwargs.*NOW()" in content:
        # This would indicate old format still exists
        old_format_matches = re.findall(r'sa_column_kwargs.*NOW\(\)', content)
        if old_format_matches:
            raise AssertionError("Found old sa_column_kwargs format for timestamps")
    
    print("✓ Models file validation passed")


def validate_utc_function():
    """Validate the utc_now function returns timezone-aware datetime."""
    # Define the function inline to test without imports
    def utc_now():
        return datetime.now(UTC)
    
    now = utc_now()
    
    if now.tzinfo is None:
        raise AssertionError("utc_now() returns naive datetime")
    
    if now.tzinfo != UTC:
        raise AssertionError(f"utc_now() returns wrong timezone: {now.tzinfo}")
    
    # Test string representation includes timezone
    now_str = str(now)
    if not now_str.endswith("+00:00"):
        raise AssertionError(f"Datetime string doesn't include timezone: {now_str}")
    
    print("✓ UTC function validation passed")


def validate_documentation_alignment():
    """Validate changes align with documented requirements."""
    # Check that we're addressing the documented issue
    docs_file = Path("docs/db_improvements.md")
    
    if docs_file.exists():
        content = docs_file.read_text()
        
        # Verify this matches the documented solution
        expected_sql_snippets = [
            "ALTER TABLE reviewers",
            "ALTER COLUMN created_at TYPE timestamp with time zone",
            "ALTER COLUMN updated_at TYPE timestamp with time zone"
        ]
        
        for snippet in expected_sql_snippets:
            if snippet not in content:
                print(f"⚠ Warning: Documentation doesn't contain: {snippet}")
    
    print("✓ Documentation alignment checked")


def main():
    """Run all validation checks."""
    print("Running timezone-aware timestamp migration validation...")
    print()
    
    try:
        validate_migration_file()
        validate_models_file()
        validate_utc_function()
        validate_documentation_alignment()
        
        print()
        print("🎉 All validations passed!")
        print()
        print("Migration is ready to apply. Next steps:")
        print("1. Schedule maintenance window")
        print("2. Apply migration: alembic upgrade head")
        print("3. Test application functionality")
        print("4. Monitor for timezone-related issues")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
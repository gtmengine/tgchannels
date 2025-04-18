#!/usr/bin/env python3
"""
Migration script for the Telegram News Aggregator database.
This script can be used to initialize or upgrade the database schema.
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_migration():
    """Run Alembic migrations."""
    try:
        # Check if versions directory exists
        versions_dir = Path("tg_news_feed/migrations/versions")
        if not versions_dir.exists():
            versions_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Created migrations versions directory")

        # Run migration
        logger.info("Running database migrations...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info(f"Migration output: {result.stdout}")
        logger.info("Migration completed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error running migrations: {str(e)}")
        return False


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1) 
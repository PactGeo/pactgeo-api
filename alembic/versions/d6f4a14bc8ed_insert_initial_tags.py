"""Insert initial tags

Revision ID: d6f4a14bc8ed
Revises: 488a7c383b09
Create Date: 2024-11-05 18:16:26.223028

"""
import json
from typing import Sequence, Union

from sqlalchemy.sql import table, column
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd6f4a14bc8ed'
down_revision: Union[str, None] = '488a7c383b09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Define the tag table structure
tag_table = table(
    'tag',
    column('id', sa.Integer),
    column('name', sa.String(length=50)),
)

def process_tag_data(tag):
    """Helper function to process JSON data into a format suitable for database insertion."""
    return {
        'name': tag['name'],
    }

def upgrade() -> None:
    # Load tag data from JSON file
    with open('api/data/tags.json') as f:
        tags = json.load(f)

    # Process the tag data
    processed_tags = [process_tag_data(tag) for tag in tags]
    
    # Insert the data into the tag table
    op.bulk_insert(tag_table, processed_tags)
    # ### end Alembic commands ###


def downgrade() -> None:
    op.execute("DELETE FROM tag WHERE name IN ('Politics', 'Economy', 'Health', 'Technology', 'Environment', 'Culture', 'Rights and Justice', 'Education', 'Work', 'Security', 'Society', 'Innovation', 'Law and Legislation', 'Geopolitics', 'Conflict', 'Migration', 'Crisis', 'Natural Resources', 'Cybersecurity', 'Poverty', 'Trade', 'Energy')")


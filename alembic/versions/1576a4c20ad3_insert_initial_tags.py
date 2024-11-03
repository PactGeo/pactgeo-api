"""Insert initial tags

Revision ID: 1576a4c20ad3
Revises: 645adfff61b9
Create Date: 2024-11-01 13:40:48.507493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import json

# revision identifiers, used by Alembic.
revision: str = '1576a4c20ad3'
down_revision: Union[str, None] = '645adfff61b9'
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


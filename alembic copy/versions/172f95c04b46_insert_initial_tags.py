"""Insert initial tags

Revision ID: new_revision_id_for_tags
Revises: new_revision_id
Create Date: 2024-09-10 15:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import json

# revision identifiers, used by Alembic.
revision: str = '172f95c04b46'
down_revision: Union[str, None] = '75ae8c5efcbc'
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

def upgrade():
    # Load tag data from JSON file
    with open('api/data/tags.json') as f:
        tags = json.load(f)

    # Process the tag data
    processed_tags = [process_tag_data(tag) for tag in tags]
    
    # Insert the data into the tag table
    op.bulk_insert(tag_table, processed_tags)

def downgrade():
    op.execute("DELETE FROM tag WHERE name IN ('Politics', 'Economy', 'Health', 'Technology', 'Environment', 'Culture', 'Rights and Justice', 'Education', 'Work', 'Security', 'Society', 'Innovation', 'Law and Legislation', 'Geopolitics', 'Conflict', 'Migration', 'Crisis', 'Natural Resources', 'Cybersecurity', 'Poverty', 'Trade', 'Energy')")

"""Insert initial users

Revision ID: 75ae8c5efcbc
Revises: d164644f6d07
Create Date: 2024-09-10 14:51:37.885703

"""
from typing import Sequence, Union

from datetime import datetime
import json
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '75ae8c5efcbc'
down_revision: Union[str, None] = 'd164644f6d07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_table = table(
    'users',
    column('id', sa.Integer),
    column('name', sa.String),
    column('email', sa.String),
    column('emailVerified', sa.DateTime),
    column('image', sa.String),
    column('birthdate', sa.DateTime),
    column('gender', sa.String),
    column('isActive', sa.Boolean),
    column('role', sa.Enum('USER', 'ADMIN', 'MODERATOR', name='userrole')),
    column('username', sa.String),
    column('country_id', sa.Integer),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime),
)

def process_user_data(user):
    """Helper function to process JSON data into a format suitable for database insertion."""
    email_verified = datetime.utcnow() if user.get('emailVerified') else None
    birthdate = datetime.strptime(user['birthdate'], "%Y-%m-%d") if 'birthdate' in user else None

    return {
        'name': user.get('name'),
        'email': user.get('email'),
        'emailVerified': email_verified,
        'image': user.get('image'),
        'birthdate': birthdate,
        'gender': user.get('gender'),
        'isActive': user.get('is_active', True),
        'role': user.get('role', 'USER'),
        'username': user.get('username'),
        'created_at': datetime.utcnow(),
        'updated_at': None,
        'country_id': None  # Assuming no country_id for now
    }

def upgrade():
    # Load user data from JSON file
    with open('api/data/users.json') as f:
        users = json.load(f)

    # Process the user data
    processed_users = [process_user_data(user) for user in users]
    
    # Insert the data into the users table
    op.bulk_insert(user_table, processed_users)

def downgrade():
    op.execute("DELETE FROM users WHERE username IN ('sebacc92', 'dailentz', 'gustavocardoso', 'adrianacastillo', 'valeriacardoso', 'cirocardoso')")
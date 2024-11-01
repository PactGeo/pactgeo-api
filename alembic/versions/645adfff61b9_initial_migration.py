"""Initial Migration

Revision ID: 645adfff61b9
Revises: 
Create Date: 2024-11-01 02:12:36.457208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = '645adfff61b9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('community',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['community.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('globalcommunity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('continent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('global_community_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['global_community_id'], ['globalcommunity.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_continent_name'), 'continent', ['name'], unique=False)
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('area', sa.Float(), nullable=True),
    sa.Column('borders', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('capital_latlng', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('capital', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('cca2', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('cca3', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('coat_of_arms_svg', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('currency_code', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('currency_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('flag', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('google_maps_link', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('idd_root', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('idd_suffixes', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('landlocked', sa.Boolean(), nullable=True),
    sa.Column('languages', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('native_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('numeric_code', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('openstreet_maps_link', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('region', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('subregion', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('timezone', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('continent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['continent_id'], ['continent.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_country_cca2'), 'country', ['cca2'], unique=False)
    op.create_index(op.f('ix_country_cca3'), 'country', ['cca3'], unique=False)
    op.create_index(op.f('ix_country_name'), 'country', ['name'], unique=False)
    op.create_table('subnation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('area', sa.Float(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('borders', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('capital', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('flag', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('iso_code', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('timezone', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('famous_landmark', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subnation_name'), 'subnation', ['name'], unique=False)
    op.create_table('users',
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
    sa.Column('emailVerified', sa.DateTime(), nullable=True),
    sa.Column('image', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('birthdate', sa.DateTime(), nullable=True),
    sa.Column('gender', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=True),
    sa.Column('isActive', sa.Boolean(), nullable=True),
    sa.Column('role', sa.Enum('USER', 'ADMIN', 'MODERATOR', name='userrole'), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('provider', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('provider_account_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('refresh_token', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('access_token', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('expires_at', sa.Integer(), nullable=True),
    sa.Column('token_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('scope', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id_token', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('session_state', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('debate',
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('dislikes_count', sa.BigInteger(), nullable=True),
    sa.Column('images', sa.JSON(), nullable=True),
    sa.Column('language', sa.Enum('EN', 'ES', 'FR', name='languagecode'), nullable=True),
    sa.Column('likes_count', sa.BigInteger(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=False),
    sa.Column('slug', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('status', sa.Enum('OPEN', 'PENDING', 'CLOSED', 'REJECTED', 'ARCHIVED', 'RESOLVED', name='debatestatus'), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('type', sa.Enum('GLOBAL', 'INTERNATIONAL', 'NATIONAL', 'SUBNATIONAL', 'SUBDIVISION', name='debatetype'), nullable=False),
    sa.Column('views_count', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('approved_by_id', sa.Integer(), nullable=True),
    sa.Column('rejected_by_id', sa.Integer(), nullable=True),
    sa.Column('approved_at', sa.DateTime(), nullable=True),
    sa.Column('rejected_at', sa.DateTime(), nullable=True),
    sa.Column('moderation_notes', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['approved_by_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['rejected_by_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_debate_created_at'), 'debate', ['created_at'], unique=False)
    op.create_index(op.f('ix_debate_slug'), 'debate', ['slug'], unique=True)
    op.create_index(op.f('ix_debate_title'), 'debate', ['title'], unique=False)
    op.create_table('poll',
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('poll_type', sa.Enum('BINARY', 'SINGLE_CHOICE', 'MULTIPLE_CHOICE', name='polltype'), nullable=False),
    sa.Column('is_anonymous', sa.Boolean(), nullable=False),
    sa.Column('ends_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('community_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'CLOSED', 'DRAFT', name='pollstatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['community_id'], ['community.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_poll_slug'), 'poll', ['slug'], unique=True)
    op.create_table('subdivision',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('area', sa.Float(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('borders', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('iso_code', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('timezone', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('famous_landmark', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('subnation_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.ForeignKeyConstraint(['subnation_id'], ['subnation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subdivision_name'), 'subdivision', ['name'], unique=False)
    op.create_table('usercommunitylink',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('community_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['community_id'], ['community.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'community_id')
    )
    op.create_table('debatechangelog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('debate_id', sa.Integer(), nullable=False),
    sa.Column('changed_by_id', sa.Integer(), nullable=False),
    sa.Column('changed_at', sa.DateTime(), nullable=False),
    sa.Column('field_changed', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('old_value', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('new_value', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('reason', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['changed_by_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['debate_id'], ['debate.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('debatecountryinvolvedlink',
    sa.Column('debate_id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.ForeignKeyConstraint(['debate_id'], ['debate.id'], ),
    sa.PrimaryKeyConstraint('debate_id', 'country_id')
    )
    op.create_table('debatesubnationinvolvedlink',
    sa.Column('debate_id', sa.Integer(), nullable=False),
    sa.Column('subnation_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['debate_id'], ['debate.id'], ),
    sa.ForeignKeyConstraint(['subnation_id'], ['subnation.id'], ),
    sa.PrimaryKeyConstraint('debate_id', 'subnation_id')
    )
    op.create_table('debatetaglink',
    sa.Column('debate_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['debate_id'], ['debate.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('debate_id', 'tag_id')
    )
    op.create_table('pointofview',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('debate_id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('subnation_id', sa.Integer(), nullable=True),
    sa.Column('subdivision_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['debate_id'], ['debate.id'], ),
    sa.ForeignKeyConstraint(['subdivision_id'], ['subdivision.id'], ),
    sa.ForeignKeyConstraint(['subnation_id'], ['subnation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('poll_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poll_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['poll_id'], ['poll.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('poll_options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('votes', sa.Integer(), nullable=False),
    sa.Column('poll_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['poll_id'], ['poll.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('poll_reactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poll_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('reaction_type', sa.Enum('LIKE', 'DISLIKE', name='reactiontype'), nullable=False),
    sa.Column('reacted_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['poll_id'], ['poll.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('poll_id', 'user_id', name='_user_poll_reaction_uc')
    )
    op.create_table('polltaglink',
    sa.Column('poll_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['poll_id'], ['poll.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('poll_id', 'tag_id')
    )
    op.create_table('opinion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('point_of_view_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(length=5000), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['point_of_view_id'], ['pointofview.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poll_id', sa.Integer(), nullable=False),
    sa.Column('option_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('voted_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['option_id'], ['poll_options.id'], ),
    sa.ForeignKeyConstraint(['poll_id'], ['poll.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('opinionvote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opinion_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['opinion_id'], ['opinion.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('opinionvote')
    op.drop_table('votes')
    op.drop_table('opinion')
    op.drop_table('polltaglink')
    op.drop_table('poll_reactions')
    op.drop_table('poll_options')
    op.drop_table('poll_comments')
    op.drop_table('pointofview')
    op.drop_table('debatetaglink')
    op.drop_table('debatesubnationinvolvedlink')
    op.drop_table('debatecountryinvolvedlink')
    op.drop_table('debatechangelog')
    op.drop_table('usercommunitylink')
    op.drop_index(op.f('ix_subdivision_name'), table_name='subdivision')
    op.drop_table('subdivision')
    op.drop_index(op.f('ix_poll_slug'), table_name='poll')
    op.drop_table('poll')
    op.drop_index(op.f('ix_debate_title'), table_name='debate')
    op.drop_index(op.f('ix_debate_slug'), table_name='debate')
    op.drop_index(op.f('ix_debate_created_at'), table_name='debate')
    op.drop_table('debate')
    op.drop_table('accounts')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_subnation_name'), table_name='subnation')
    op.drop_table('subnation')
    op.drop_index(op.f('ix_country_name'), table_name='country')
    op.drop_index(op.f('ix_country_cca3'), table_name='country')
    op.drop_index(op.f('ix_country_cca2'), table_name='country')
    op.drop_table('country')
    op.drop_index(op.f('ix_continent_name'), table_name='continent')
    op.drop_table('continent')
    op.drop_table('tag')
    op.drop_table('globalcommunity')
    op.drop_table('community')
    # ### end Alembic commands ###

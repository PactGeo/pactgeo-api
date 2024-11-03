"""Insert initial communities

Revision ID: 9a43eb99a190
Revises: 1576a4c20ad3
Create Date: 2024-11-01 18:50:57.460758

"""
from typing import Sequence, Union

import json
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '9a43eb99a190'
down_revision: Union[str, None] = '1576a4c20ad3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

communities_table = table(
    'community',
    column('id', sa.Integer),
    column('name', sa.String),
    column('type', sa.String),
    column('description', sa.String),
    column('parent_id', sa.Integer),
    column('created_at', sa.DateTime),
)

globalcommunity_table = table(
    'globalcommunity',
    column('id', sa.Integer),
    column('name', sa.String),
    column('description', sa.String),
)

continent_table = table(
    'continent',
    column('id', sa.Integer),
    column('name', sa.String),
    column('description', sa.String),
)

country_table = table(
    'country',
    column('id', sa.Integer),
    column('name', sa.String),
    column('area', sa.Float),
    column('borders', sa.String),
    column('capital_latlng', sa.String),
    column('capital', sa.String),
    column('cca2', sa.String),
    column('cca3', sa.String),
    column('coat_of_arms_svg', sa.String),
    column('continent', sa.String),
    column('currency_code', sa.String),
    column('currency_name', sa.String),
    column('flag', sa.String),
    column('google_maps_link', sa.String),
    column('idd_root', sa.String),
    column('idd_suffixes', sa.String),
    column('landlocked', sa.Boolean),
    column('languages', sa.String),
    column('native_name', sa.String),
    column('numeric_code', sa.String),
    column('openstreet_maps_link', sa.String),
    column('population', sa.Integer),
    column('region', sa.String),
    column('status', sa.String),
    column('subregion', sa.String),
    column('timezone', sa.String),
)

subnation_table = table(
    'subnation',
    column('id', sa.Integer),
    column('name', sa.String),
    column('country_id', sa.Integer),
    column('area', sa.Float),
    column('population', sa.Integer),
    column('borders', sa.String),
    column('capital', sa.String),
    column('flag', sa.String),
    column('iso_code', sa.String),
    column('timezone', sa.String),
    column('famous_landmark', sa.String),
)

subdivision_table = table(
    'subdivision',
    column('id', sa.Integer),
    column('name', sa.String),
    column('subnation_id', sa.Integer),
    column('country_id', sa.Integer),
    column('area', sa.Float),
    column('population', sa.Integer),
    column('borders', sa.String),
    column('iso_code', sa.String),
    column('timezone', sa.String),
    column('famous_landmark', sa.String),
)

def process_community_data(community, community_type, parent_id=None):
    """Helper function to process JSON data into a format suitable for database insertion."""
    return {
        'name': community['name'],
        'type': community_type,
        'description': community.get('description'),
        'parent_id': parent_id,
    }

def process_country_data(country):
    """Helper function to process JSON data into a format suitable for database insertion."""
    return {
        'name': country['name']['common'],
        'area': country.get('area'),
        'borders': ','.join(country.get('borders', [])),
        'capital_latlng': ','.join(map(str, country.get('capitalInfo', {}).get('latlng', []))),
        'capital': ','.join(country.get('capital', [])),
        'cca2': country.get('cca2'),
        'cca3': country.get('cca3'),
        'coat_of_arms_svg': country.get('coatOfArms', {}).get('svg'),
        'continent': ','.join(country.get('continents', [])),
        'currency_code': list(country.get('currencies', {}).keys())[0] if country.get('currencies') else None,
        'currency_name': list(country.get('currencies', {}).values())[0].get('name') if country.get('currencies') else None,
        'flag': country.get('flag'),
        'google_maps_link': country.get('maps', {}).get('googleMaps'),
        'idd_root': country.get('idd', {}).get('root'),
        'idd_suffixes': ','.join(country.get('idd', {}).get('suffixes', [])),
        'landlocked': country.get('landlocked'),
        'languages': ','.join(country.get('languages', {}).values()),
        'native_name': ','.join([name.get('official') for name in country.get('name', {}).get('nativeName', {}).values()]) if country.get('name', {}).get('nativeName') else None,
        'numeric_code': country.get('ccn3'),
        'openstreet_maps_link': country.get('maps', {}).get('openStreetMaps'),
        'population': country.get('population'),
        'region': country.get('region'),
        'status': country.get('status'),
        'subregion': country.get('subregion'),
        'timezone': ','.join(country.get('timezones', [])),
    }

def process_subnation_data(subnation, country_id):
    return {
        'name': subnation['name'],
        'country_id': country_id,
        'area': subnation.get('area'),
        'population': subnation.get('population'),
        'borders': ','.join(subnation.get('borders', [])),
        'capital': subnation.get('capital'),
        'flag': subnation.get('flag'),
        'iso_code': subnation.get('additional_info', {}).get('iso_code'),
        'timezone': subnation.get('additional_info', {}).get('timezone'),
        'famous_landmark': subnation.get('additional_info', {}).get('famous_landmark'),
    }

def process_subdivision_data(subdivision, subnation_id, country_id):
    return {
        'name': subdivision['name'],
        'subnation_id': subnation_id,
        'country_id': country_id,
        'area': subdivision.get('area'),
        'population': subdivision.get('population'),
        'borders': ','.join(subdivision.get('borders', [])),
        'iso_code': subdivision.get('additional_info', {}).get('iso_code'),
        'timezone': subdivision.get('additional_info', {}).get('timezone'),
        'famous_landmark': subdivision.get('additional_info', {}).get('famous_landmark'),
    }

def upgrade() -> None:
    # Create global community
    global_community = {
        'name': 'Global',
        'type': 'global',
        'description': 'Global community encompassing all continents and countries.',
        'parent_id': None,
    }

    # Create Global Community
    op.bulk_insert(globalcommunity_table, [global_community])
    op.bulk_insert(communities_table, [global_community])

    # Create Continents Community
    with open('api/data/continents.json') as f:
        continents = json.load(f)
    
    continent_records = []
    continent_communities = []
    for continent in continents:
        continent_record = {
            'name': continent['name'],
            'description': continent['description'],
            'parent_id': 1, # Global community be 1 ID
        }
        continent_records.append(continent_record)

        community_data = process_community_data(
            community=continent,
            community_type='continent',
            parent_id=1,
        )
        continent_communities.append(community_data)

    op.bulk_insert(continent_table, continent_records)
    op.bulk_insert(communities_table, continent_communities)

    # Cargar datos desde el archivo JSON
    with open('api/data/countries.json') as f:
        countries = json.load(f)

    processed_countries = [process_country_data(country) for country in countries]
    op.bulk_insert(country_table, processed_countries)

    # Crear comunidades para países
    country_communities = [
        process_community_data(
            community=country,
            community_type='country',
            parent_id=None,
        ) for country in processed_countries]
    op.bulk_insert(communities_table, country_communities)

    # Obtener conexiones y construir mapas de ID
    conn = op.get_bind()

    # Mapa de nombre de país a ID de país
    country_name_to_country_id = dict(
        conn.execute(
            sa.select(country_table.c.name, country_table.c.id)
        ).fetchall()
    )

    # Mapa de (nombre, tipo) a ID de comunidad
    community_key_to_id = dict(
        ((name, type_), id_) for name, type_, id_ in conn.execute(
            sa.select(communities_table.c.name, communities_table.c.type, communities_table.c.id)
        )
    )

    # Mapa de ID de país a ID de comunidad
    country_id_to_community_id = {}
    for country_name, country_id in country_name_to_country_id.items():
        community_id = community_key_to_id.get((country_name, 'country'))
        if community_id:
            country_id_to_community_id[country_id] = community_id

    # Procesar subnaciones
    with open('api/data/subnations.json') as f:
        subnations = json.load(f)

    processed_subnations = []
    for subnation in subnations:
        country_name = subnation['country']
        country_id = country_name_to_country_id.get(country_name)
        if not country_id:
            continue  # Omitir si el país no se encuentra
        processed_subnation = process_subnation_data(subnation, country_id)
        processed_subnations.append(processed_subnation)

    op.bulk_insert(subnation_table, processed_subnations)

    # Crear comunidades para subnaciones
    subnation_communities = []
    for subnation in processed_subnations:
        country_id = subnation['country_id']
        parent_community_id = country_id_to_community_id.get(country_id)
        community_data = process_community_data(
            community=subnation,
            community_type='subnation',
            parent_id=parent_community_id,
        )
        subnation_communities.append(community_data)

    op.bulk_insert(communities_table, subnation_communities)

    # Actualizar mapas con subnaciones
    subnation_name_to_subnation_id = dict(
        conn.execute(
            sa.select(subnation_table.c.name, subnation_table.c.id)
        ).fetchall()
    )

    community_key_to_id.update(
        ((name, type_), id_) for name, type_, id_ in conn.execute(
            sa.select(communities_table.c.name, communities_table.c.type, communities_table.c.id)
        )
    )

    subnation_id_to_community_id = {}
    for subnation_name, subnation_id in subnation_name_to_subnation_id.items():
        community_id = community_key_to_id.get((subnation_name, 'subnation'))
        if community_id:
            subnation_id_to_community_id[subnation_id] = community_id

    # Procesar subdivisiones
    with open('api/data/subdivisions.json') as f:
        subdivisions = json.load(f)

    processed_subdivisions = []
    for subdivision in subdivisions:
        country_name = subdivision['country']
        subnation_name = subdivision['subnation']
        country_id = country_name_to_country_id.get(country_name)
        subnation_id = subnation_name_to_subnation_id.get(subnation_name)
        if not country_id or not subnation_id:
            continue  # Omitir si el país o la subnación no se encuentran
        processed_subdivision = process_subdivision_data(subdivision, subnation_id, country_id)
        processed_subdivisions.append(processed_subdivision)

    op.bulk_insert(subdivision_table, processed_subdivisions)

    # Crear comunidades para subdivisiones
    subdivision_communities = []
    for subdivision in processed_subdivisions:
        subnation_id = subdivision['subnation_id']
        parent_community_id = subnation_id_to_community_id.get(subnation_id)
        community_data = process_community_data(
            community=subdivision,
            community_type='subdivision',
            parent_id=parent_community_id,
        )
        subdivision_communities.append(community_data)

    op.bulk_insert(communities_table, subdivision_communities)

def downgrade() -> None:
    op.execute("DELETE FROM communities WHERE type IN ('country', 'subnation', 'subdivision')")
    op.execute("DELETE FROM subdivision WHERE name IN (SELECT name FROM subdivision)")
    op.execute("DELETE FROM subnation WHERE name IN (SELECT name FROM subnation)")
    op.execute("DELETE FROM country WHERE name IN (SELECT name FROM country)")
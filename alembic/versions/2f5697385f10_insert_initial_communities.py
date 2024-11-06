"""Insert initial communities

Revision ID: 2f5697385f10
Revises: d6f4a14bc8ed
Create Date: 2024-11-05 18:21:23.192021

"""
import json
from typing import Union, Sequence

from sqlalchemy.sql import table, column
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2f5697385f10'
down_revision: Union[str, None] = 'd6f4a14bc8ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


communities_table = table(
    'community',
    column('id', sa.Integer),
    column('name', sa.String),
    column('level', sa.String),
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
    column('continent_id', sa.Integer),
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


def process_community_data(community, community_level, parent_id=None):
    """Helper function to process JSON data into a format suitable for database insertion."""
    return {
        'name': community['name'],
        'level': community_level,
        'description': community.get('description'),
        'parent_id': parent_id,
    }


def process_country_data(country, continent_name_to_id):
    """Helper function to process JSON data into a format suitable for database insertion."""
    continent_names = country.get('continents', [])
    print('continent_names::')
    print(continent_names)
    continent_name = continent_names[0] if continent_names else None
    print('continent_name::')
    print(continent_name)
    continent_id = continent_name_to_id.get(continent_name) if continent_name else None
    print('continent_id::')
    print(continent_id)
    return {
        'name': country['name']['common'],
        'area': country.get('area'),
        'borders': ','.join(country.get('borders', [])),
        'capital_latlng': ','.join(map(str, country.get('capitalInfo', {}).get('latlng', []))),
        'capital': ','.join(country.get('capital', [])),
        'cca2': country.get('cca2'),
        'cca3': country.get('cca3'),
        'coat_of_arms_svg': country.get('coatOfArms', {}).get('svg'),
        'continent_id': continent_id,
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
        'timezone': ','.join(country.get('timezones', []))
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
    # Crear comunidad global sin especificar 'id'
    planet_community = {
        'name': 'Earth',
        'level': 'GLOBAL',
        'description': 'Global community encompassing all continents and countries.',
        'parent_id': None,
    }

    # Insertar en globalcommunity_table
    op.bulk_insert(globalcommunity_table, [planet_community])

    # Obtener el 'id' generado para la comunidad global en 'globalcommunity' table
    conn = op.get_bind()
    result = conn.execute(sa.select(globalcommunity_table.c.id).where(globalcommunity_table.c.name == 'Earth'))
    global_community_id = result.scalar()

    # Insertar en communities_table sin especificar 'id'
    community_data = {
        'name': 'Global',
        'level': 'GLOBAL',
        'description': 'Global community encompassing all continents and countries.',
        'parent_id': None,
    }
    op.bulk_insert(communities_table, [community_data])

    # Obtener el 'id' generado para la comunidad global en 'community' table
    result = conn.execute(sa.select(communities_table.c.id).where(communities_table.c.name == 'Global'))
    global_community_community_id = result.scalar()

    # Crear comunidades de continentes
    with open('api/data/continents.json') as f:
        continents = json.load(f)
    continent_records = []
    continent_communities = []
    for continent in continents:
        continent_record = {
            'name': continent['name'],
            'description': continent['description'],
        }
        continent_records.append(continent_record)

        # Asignar 'parent_id' a la comunidad global
        community_data = process_community_data(
            community=continent,
            community_level='CONTINENT',
            parent_id=global_community_community_id,  # Referencia correcta
        )
        continent_communities.append(community_data)

    op.bulk_insert(continent_table, continent_records)
    op.bulk_insert(communities_table, continent_communities)

    # Mapeo de nombre de continente a 'continent.id'
    continent_name_to_id = dict(
        conn.execute(
            sa.select(continent_table.c.name, continent_table.c.id)
        ).fetchall()
    )
    print('continent_name_to_id::')
    print(continent_name_to_id)

    # Mapeo de 'continent_id' a 'community_id' de los continentes en 'community' table
    continent_id_to_community_id = {}
    for continent_name, continent_id in continent_name_to_id.items():
        # Obtener el 'id' de la comunidad del continente
        community_id = conn.execute(
            sa.select(communities_table.c.id).where(
                sa.and_(
                    communities_table.c.name == continent_name,
                    communities_table.c.level == 'CONTINENT'
                )
            )
        ).scalar()
        continent_id_to_community_id[continent_id] = community_id

    # Cargar datos desde el archivo JSON de países
    with open('api/data/countries.json') as f:
        countries = json.load(f)

    # Procesar y insertar países en la tabla 'country'
    processed_countries = [process_country_data(country, continent_name_to_id) for country in countries]
    op.bulk_insert(country_table, processed_countries)

    # Crear comunidades para países con 'parent_id' apuntando al 'id' de la comunidad del continente
    country_communities = []
    for country in processed_countries:
        continent_id = country['continent_id']
        if continent_id:
            continent_community_id = continent_id_to_community_id.get(continent_id)
            if not continent_community_id:
                raise ValueError(f"Community for continent_id {continent_id} not found.")
        else:
            continent_community_id = None  # Manejar si no hay continente

        # Crear la comunidad del país con el 'parent_id' correcto
        community = {
            'name': country['name'],
            'level': 'NATIONAL',
            'description': f"Nacional community for {country['name']}.",
            'parent_id': continent_community_id,
        }
        country_communities.append(community)

    op.bulk_insert(communities_table, country_communities)

    # Mapeo de nombre de país a 'community.id'
    country_name_to_community_id = dict(
        conn.execute(
            sa.select(communities_table.c.name, communities_table.c.id).where(communities_table.c.level == 'NATIONAL')
        ).fetchall()
    )

    # Procesar subnaciones
    with open('api/data/subnations.json') as f:
        subnations = json.load(f)

    processed_subnations = []
    for subnation in subnations:
        country_name = subnation['country']
        community_id = country_name_to_community_id.get(country_name)
        if not community_id:
            continue  # Omitir si la comunidad del país no se encuentra
        # Obtener el 'country_id' basado en el nombre del país
        country_id = conn.execute(
            sa.select(country_table.c.id).where(country_table.c.name == country_name)
        ).scalar()
        if not country_id:
            continue  # Omitir si el país no se encuentra
        processed_subnation = process_subnation_data(subnation, country_id=country_id)
        processed_subnations.append(processed_subnation)

    op.bulk_insert(subnation_table, processed_subnations)

    # Crear comunidades para subnaciones
    subnation_communities = []
    for subnation in processed_subnations:
        country_id = subnation['country_id']
        # Obtener el nombre del país para mapear al 'community_id'
        country_name = conn.execute(
            sa.select(country_table.c.name).where(country_table.c.id == country_id)
        ).scalar()
        parent_community_id = country_name_to_community_id.get(country_name)
        if not parent_community_id:
            continue  # Omitir si no se encuentra la comunidad del país
        community_data = process_community_data(
            community=subnation,
            community_level='SUBNATIONAL',
            parent_id=parent_community_id,
        )
        subnation_communities.append(community_data)

    op.bulk_insert(communities_table, subnation_communities)

    # Mapeo de nombre de subnación a 'community.id'
    subnation_name_to_community_id = dict(
        conn.execute(
            sa.select(communities_table.c.name, communities_table.c.id).where(communities_table.c.level == 'SUBNATIONAL')
        ).fetchall()
    )

    # Procesar subdivisiones
    with open('api/data/subdivisions.json') as f:
        subdivisions = json.load(f)

    processed_subdivisions = []
    for subdivision in subdivisions:
        country_name = subdivision['country']
        subnation_name = subdivision['subnation']
        # Obtener el 'country_id' basado en el nombre del país
        country_id = conn.execute(
            sa.select(country_table.c.id).where(country_table.c.name == country_name)
        ).scalar()
        # Obtener el 'subnation_id' basado en el nombre de la subnación
        subnation_id = conn.execute(
            sa.select(subnation_table.c.id).where(subnation_table.c.name == subnation_name)
        ).scalar()
        if not country_id or not subnation_id:
            continue  # Omitir si el país o la subnación no se encuentran
        processed_subdivision = process_subdivision_data(subdivision, subnation_id, country_id)
        processed_subdivisions.append(processed_subdivision)

    op.bulk_insert(subdivision_table, processed_subdivisions)

    # Crear comunidades para subdivisiones
    subdivision_communities = []
    for subdivision in processed_subdivisions:
        subnation_id = subdivision['subnation_id']
        # Obtener el 'name' de la subnación para mapear al 'community_id'
        subnation_name = conn.execute(
            sa.select(subnation_table.c.name).where(subnation_table.c.id == subnation_id)
        ).scalar()
        parent_community_id = subnation_name_to_community_id.get(subnation_name)
        if not parent_community_id:
            continue  # Omitir si no se encuentra la comunidad de la subnación
        community_data = process_community_data(
            community=subdivision,
            community_level='LOCAL',
            parent_id=parent_community_id,
        )
        subdivision_communities.append(community_data)

    op.bulk_insert(communities_table, subdivision_communities)


def downgrade() -> None:
    op.execute("DELETE FROM communities WHERE level IN ('NATIONAL', 'SUBNATIONAL', 'LOCAL')")
    op.execute("DELETE FROM subdivision WHERE name IN (SELECT name FROM subdivision)")
    op.execute("DELETE FROM subnation WHERE name IN (SELECT name FROM subnation)")
    op.execute("DELETE FROM country WHERE name IN (SELECT name FROM country)")
    op.execute("DELETE FROM continent WHERE name IN (SELECT name FROM continent)")
    op.execute("DELETE FROM globalcommunity WHERE name = 'Earth'")
    op.execute("DELETE FROM community WHERE name = 'Global'")

import json
from sqlmodel import Session, select
from fastapi import HTTPException, status
from api.database import engine
from api.database import create_db_and_tables
from api.utils.logger import logger_config
from api.public.country.models import Country
from api.public.user.models import User, UserCreate
from api.public.tag.models import TagCreate
from api.public.debate.models import DebateCreate
from api.public.country.crud import create_country
from api.public.subnation.crud import create_subnation
from api.public.user.crud import create_user
from api.public.tag.crud import create_tag
from api.public.debate.crud import create_debate
from api.public.point_of_view.crud import create_points_of_view

logger = logger_config(__name__)
def load_json_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_countries(db):
    countries_data = load_json_file('api/data/countries.json')
    countries = []
    for country_data in countries_data:
        country = {
            "name": country_data["name"]["common"],
            "area": country_data.get("area"),
            "borders": ', '.join(country_data.get("borders", [])),
            "capital_latlng": ', '.join(map(str, country_data.get("capitalInfo", {}).get("latlng", []))),
            "capital": ', '.join(country_data.get("capital", [])),
            "cca2": country_data.get("cca2"),
            "cca3": country_data.get("cca3"),
            "coat_of_arms_svg": country_data.get("coatOfArms", {}).get("svg"),
            "continent": ', '.join(country_data.get("continents", [])),
            "currency_code": ', '.join(country_data.get("currencies", {}).keys()),
            "currency_name": ', '.join([currency.get("name") for currency in country_data.get("currencies", {}).values()]),
            "flag": country_data.get("flag"),
            "google_maps_link": country_data.get("maps", {}).get("googleMaps"),
            "idd_root": country_data.get("idd", {}).get("root"),
            "idd_suffixes": ', '.join(country_data.get("idd", {}).get("suffixes", [])),
            "landlocked": country_data.get("landlocked"),
            "languages": ', '.join(country_data.get("languages", {}).values()),
            "native_name": ', '.join([f"{lang}: {info['official']}" for lang, info in country_data.get("name", {}).get("nativeName", {}).items()]),
            "numeric_code": country_data.get("ccn3"),
            "openstreet_maps_link": country_data.get("maps", {}).get("openStreetMaps"),
            "population": country_data.get("population"),
            "region": country_data.get("region"),
            "status": country_data.get("status"),
            "subregion": country_data.get("subregion"),
            "timezone": ', '.join(country_data.get("timezones", [])),
        }
        new_country = create_country(db, country)
        countries.append(new_country)
    logger.info("=========== MOCK COUNTRIES CREATED ===========")
    return countries

def create_subnations(db):
    subnations_data = load_json_file('api/data/subnations.json')
    subnations = []
    for subnation_data in subnations_data:
        country = db.exec(select(Country).where(Country.cca2 == subnation_data["country"])).first()
        subnation = {
            "name": subnation_data["name"],
            "area": subnation_data.get("area"),
            "borders": ', '.join(subnation_data.get("borders", [])),
            "capital": subnation_data.get("capital"),
            "flag": subnation_data.get("flag"),
            "iso_code": subnation_data.get("additional_info").get("iso_code"),
            "timezone": subnation_data.get("additional_info").get("timezone"),
            "famous_landmark": subnation_data.get("additional_info").get("famous_landmark"),
            "country_id": country.id
        }
        new_subnation = create_subnation(db, subnation)
        subnations.append(new_subnation)
    logger.info("=========== MOCK SUBNATIONS CREATED ===========")
    return subnations

def create_all_tags(db):
    tags_data = load_json_file('api/data/tags.json')
    for tag_data in tags_data:
        tag = TagCreate(name=tag_data["name"])
        create_tag(tag, db)
    logger.info("=========== MOCK TAGS CREATED ===========")

def create_users(db, countries):
    users = load_json_file('api/data/users.json')
    for user_data in users:
        user = UserCreate(
            username=user_data.get("username"),
            email=user_data.get("email"),
            name=user_data.get("name"),
            role=user_data.get("role"),
            is_active=user_data.get("is_active"),
            birthdate=user_data.get("birthdate"),
            image=user_data.get("image"),
            gender=user_data.get("gender"),
            country_id=countries[0].id
        )
        create_user(user, db)
    logger.info("=========== MOCK USERS CREATED ===========")

def create_debates(db):
    debates_data = load_json_file('api/data/debates.json')
    for debate_data in debates_data:
        creator = db.exec(select(User).where(User.username == debate_data["creator_username"])).first()
        if not creator:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        debate = DebateCreate(
            title=debate_data["title"],
            description=debate_data["description"],
            type=debate_data["type"],
            public=debate_data["public"],
            images=debate_data["images"],
            tags=debate_data["tags"],
            status=debate_data["status"],
            language=debate_data["language"],
            creator_id=creator.id,
            countries_involved=debate_data.get("countries_involved", [])
        )
        created_debate = create_debate(debate, db)
        print('created_debate')
        print(created_debate)
        # # Crear puntos de vista para el debate, si aplica
        # participating_communities=debate_data.get("participating_communities")
        # create_points_of_view(created_debate, db, participating_communities)

    logger.info("=========== MOCK DEBATES CREATED ===========")

def create_db_and_insert_data():
    create_db_and_tables()
    # Usar una única sesión para todas las operaciones
    with Session(engine) as db:
        countries = create_countries(db)
        create_subnations(db)
        create_all_tags(db)
        create_users(db, countries)
        # create_debates(db)
        db.commit()
        print("======= DATOS INSERTADOS CORRECTAMENTE =======")

if __name__ == "__main__":
    create_db_and_insert_data()

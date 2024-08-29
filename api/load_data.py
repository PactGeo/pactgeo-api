import json
from sqlmodel import Session, select
from api.database import engine
from api.database import create_db_and_tables
from api.utils.security import get_password_hash
from api.utils.logger import logger_config
from api.public.user.models import User, UserCreate
from api.public.tag.models import Tag, TagCreate
from api.public.country.crud import create_country
from api.public.user.crud import create_user
from api.public.tag.crud import create_tag

logger = logger_config(__name__)
def load_json_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_countries():
    with Session(engine) as session:
        countries = load_json_file('api/data/countries.json')
        for country_data in countries:
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
            create_country(session, country)
        logger.info("=========== MOCK COUNTRIES CREATED ===========")

def create_users():
    with Session(engine) as session:
        users = load_json_file('api/data/users.json')
        for user_data in users:
            user = UserCreate(
                username=user_data.get("username"),
                email=user_data.get("email"),
                full_name=user_data.get("full_name"),
                role=user_data.get("role"),
                is_active=user_data.get("is_active"),
                birthdate=user_data.get("birthdate"),
                image_url=user_data.get("image_url")
            )
            create_user(user, session)
        logger.info("=========== MOCK USERS CREATED ===========")

def create_all_tags():
    with Session(engine) as session:
        tags = load_json_file('api/data/tags.json')
        for tag in tags:
            tag = TagCreate(
                name=tag["name"]
            )
            create_tag(tag, session)
        logger.info("=========== MOCK TAGS CREATED ===========")

def create_db_and_insert_data():
    create_db_and_tables()
    create_countries()
    create_users()
    create_all_tags()

    # Abrir una sesión
    with Session(engine) as session:

        print("Datos insertados correctamente.")

if __name__ == "__main__":
    create_db_and_insert_data()

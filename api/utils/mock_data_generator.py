
import json
from random import choice
from datetime import datetime
from sqlmodel import Session, select

from api.database import engine
from api.public.hero.models import Hero
from api.public.team.models import Team
from api.public.community.models import Community
from api.public.tag.models import Tag
from api.utils.logger import logger_config
from api.public.user.models import User
from api.public.debate.models import Debate
from api.utils.security import get_password_hash

logger = logger_config(__name__)

def load_json_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_global_debates():
    with Session(engine) as session:
        # Obtener la comunidad global
        global_community = session.exec(select(Community).where(Community.type == "world")).first()
        if not global_community:
            logger.error("No global community found. Make sure to create communities first.")
            return        
        users = session.exec(select(User)).all()
        if not users:
            logger.error("No users found. Make sure to create users first.")
            return
        debates = load_json_file('api/data/debates.json')
        for debate_data in debates:
            user = choice(users)  # Select a random user
            debate = Debate(
                creator_id=user.id,
                community_id=global_community.id,
                type=debate_data["type"],
                title=debate_data["title"],
                description=debate_data["description"],
                image_url=debate_data["image_url"],
                created_at=datetime.utcnow(),
            )
            session.add(debate)
            session.commit()
            session.refresh(debate)
            logger.info("Debate '%s' created by user '%s'.", debate.title, user.username)

        logger.info("=========== MOCK GLOBAL DEBATES CREATED ===========")

def create_heroes_and_teams():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        wornderful_league = Team(
            name="Wonderful-League", headquarters="Fortress of Solitude"
        )

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            age=24,
            teams=[team_z_force, team_preventers],
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            teams=[team_preventers],
        )
        hero_spider_boy = Hero(
            name="Spider-Boy",
            secret_name="Pedro Parqueador",
            age=37,
            teams=[team_preventers],
        )
        hero_super_good_boy = Hero(
            name="Super-Good-Boy",
            secret_name="John Goodman",
            age=30,
            teams=[wornderful_league, team_z_force],
        )

        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.add(hero_super_good_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)
        session.refresh(hero_super_good_boy)

        logger.info("=========== MOCK DATA CREATED ===========")
        logger.info("Deadpond %s", hero_deadpond)
        logger.info("Deadpond teams %s", hero_deadpond.teams)
        logger.info("Rusty-Man %s", hero_rusty_man)
        logger.info("Rusty-Man Teams %s", hero_rusty_man.teams)
        logger.info("Spider-Boy %s", hero_spider_boy)
        logger.info("Spider-Boy Teams %s", hero_spider_boy.teams)
        logger.info("Super-Good-Boy %s", hero_super_good_boy)
        logger.info("Super-Good-Boy Teams: %s", hero_super_good_boy.teams)
        logger.info("===========================================")

def create_world_community(session: Session):
    community_world = Community(name="Geo", type="world", description="The entire world")
    session.add(community_world)
    session.commit()
    session.refresh(community_world)
    return community_world

def create_continents(session: Session, world_community: Community):
    continents = load_json_file('api/data/continents.json')
    continent_communities = []
    for continent in continents:
        community = Community(
            name=continent["name"],
            type="continent",
            description=continent["description"],
            parent_id=world_community.id
        )
        session.add(community)
        session.commit()
        session.refresh(community)
        continent_communities.append(community)
    return continent_communities

def create_countries(session: Session, continent_communities: list):
    countries = load_json_file('api/data/countries.json')
    for country in countries:
        continent = next(c for c in continent_communities if c.name == country["continent"])
        community = Community(
            name=country["name"],
            type="country",
            description=country["description"],
            parent_id=continent.id
        )
        session.add(community)
        session.commit()
        session.refresh(community)

def create_all_communities():
    with Session(engine) as session:
        world_community = create_world_community(session)
        continent_communities = create_continents(session, world_community)
        create_countries(session, continent_communities)
        logger.info("=========== MOCK COMMUNITIES CREATED ===========")

from sqlmodel import Session, select
from api.public.debate.models import Debate
from api.public.point_of_view.models import PointOfView
from api.public.country.models import Country

def create_points_of_view(debate: Debate, session: Session, participating_communities: list[str] = None):
    if not debate.id:
        raise ValueError("Debate ID is missing")
    # Logic to create points of view based on the type of debate
    if debate.type == "global":
        countries = session.exec(select(Country)).all()
        for country in countries:
            pov = PointOfView(name=country.name, debate_id=debate.id)
            session.add(pov)
    elif debate.type == "international" and participating_communities:
        for country in participating_communities:
            pov = PointOfView(name=country, debate_id=debate.id)
            session.add(pov)
    elif debate.type == "national" and participating_communities:
        for subnational in participating_communities:
            pov = PointOfView(name=subnational, debate_id=debate.id)
            session.add(pov)
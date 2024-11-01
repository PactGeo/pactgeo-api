from sqlmodel import Field, SQLModel
class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)
class PollTagLink(SQLModel, table=True):
    poll_id: int | None = Field(default=None, foreign_key="poll.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)
class DebateTagLink(SQLModel, table=True):
    debate_id: int | None = Field(default=None, foreign_key="debate.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)

class UserCommunityLink(SQLModel, table=True):
    user_id: int | None = Field(foreign_key="users.id", primary_key=True)
    community_id: int | None = Field(foreign_key="communities.id", primary_key=True)

class DebateCountryInvolvedLink(SQLModel, table=True):
    debate_id: int | None = Field(foreign_key="debate.id", primary_key=True)
    country_id: int | None = Field(foreign_key="country.id", primary_key=True)

class DebateSubnationInvolvedLink(SQLModel, table=True):
    debate_id: int | None = Field(foreign_key="debate.id", primary_key=True)
    subnation_id: int | None = Field(foreign_key="subnation.id", primary_key=True)
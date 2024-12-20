from sqlmodel import Field, SQLModel
class PollTagLink(SQLModel, table=True):
    poll_id: int | None = Field(default=None, foreign_key="poll.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)
class PollCommunityLink(SQLModel, table=True):
    poll_id: int = Field(foreign_key="poll.id", primary_key=True)
    community_id: int = Field(foreign_key="community.id", primary_key=True)
class DebateTagLink(SQLModel, table=True):
    debate_id: int | None = Field(default=None, foreign_key="debate.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)

class UserCommunityLink(SQLModel, table=True):
    __tablename__ = "usercommunitylink"
    user_id: int | None = Field(foreign_key="users.id", primary_key=True)
    community_id: int | None = Field(foreign_key="community.id", primary_key=True)

class DebateCountryInvolvedLink(SQLModel, table=True):
    debate_id: int | None = Field(foreign_key="debate.id", primary_key=True)
    country_id: int | None = Field(foreign_key="country.id", primary_key=True)

class DebateSubnationInvolvedLink(SQLModel, table=True):
    debate_id: int | None = Field(foreign_key="debate.id", primary_key=True)
    subnation_id: int | None = Field(foreign_key="subnation.id", primary_key=True)

class UserFollowLink(SQLModel, table=True):
    __tablename__ = "user_follow_link"
    follower_id: int = Field(foreign_key="users.id", primary_key=True)
    followed_id: int = Field(foreign_key="users.id", primary_key=True)
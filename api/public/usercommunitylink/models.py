from sqlmodel import SQLModel, Field

class UserCommunityLink(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    community_id: int = Field(foreign_key="community.id", primary_key=True)

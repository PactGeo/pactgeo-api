from sqlmodel import SQLModel, Field

class DebateTagLink(SQLModel, table=True):
    debate_id: int | None = Field(default=None, foreign_key="debate.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)

from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Report(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content_type: str = Field(max_length=50)  # 'poll', 'debate', 'project'
    content_id: int = Field()  # ID of the poll/discussion/project
    reason: str = Field(max_length=100)  # Reason for the report
    description: str = Field(default=None, max_length=500)  # Optional
    user_id: int = Field(foreign_key="users.id")  # User who reports
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="reports")

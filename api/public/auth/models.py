from typing import Optional
from sqlmodel import SQLModel

class TokenRequest(SQLModel):
    provider: str
    providerAccountId: str
    email: Optional[str] = None
    name: Optional[str] = None
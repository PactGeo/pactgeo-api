from typing import Optional
from pydantic import BaseModel

class TokenRequest(BaseModel):
    provider: str
    providerAccountId: str
    email: Optional[str] = None
    name: Optional[str] = None
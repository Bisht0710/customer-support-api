from pydantic import BaseModel, Field
from typing import Optional, Literal


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    status: Literal["Open", "In Progress", "Closed"]
    tags: Optional[str] = ""


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    tags: str
    created_at: str
    response_deadline: str
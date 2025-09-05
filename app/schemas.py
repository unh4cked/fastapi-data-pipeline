from __future__ import annotations

from pydantic import BaseModel

class ItemOut(BaseModel):
    id: int
    ext_id: int | None
    title: str
    body: str
    user_id: int | None

    class Config:
        from_attributes = True

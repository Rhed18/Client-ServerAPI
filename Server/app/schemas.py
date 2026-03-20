from pydantic import BaseModel
from typing import Optional


class OrderCreate(BaseModel):
    customer: Optional[str] = None
    bw_pages: int = 0
    color_pages: int = 0
    photo_pages: int = 0


class OrderOut(OrderCreate):
    id: int
    total: float
    status: str
    created_at: str
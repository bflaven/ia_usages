from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Track(BaseModel):
    id: Optional[int] = None
    title: str
    artist: str
    duration: float
    last_play: datetime
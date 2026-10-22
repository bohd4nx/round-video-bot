from pydantic import BaseModel


class MediaInfo(BaseModel):
    duration: float
    has_audio: bool


class Segment(BaseModel):
    index: int
    start: float
    duration: float

# pydantic models for tagging API

from datetime import datetime, timezone
from enum import Enum
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator

class ArtifactType(str, Enum):
    SPEECH = 'speech'
    IMAGE = 'image'

class TagCategory(str, Enum):
    ANIMAL = 'animal'
    LOCATION = 'location'
    COLOR = 'color'
    GENRE = 'genre'
    TOPIC = 'topic'
    TIME_OF_DAY = 'time_of_day'
    OTHER = 'other'

class Tag(BaseModel):
    category: TagCategory
    value: str

    @field_validator('value')
    @classmethod
    def value_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Tag value must not be empty')
        return v.strip()
    
    @field_validator('value')
    @classmethod
    def normalize_value(cls, v):
        return v.lower().strip()
    
class Artifact(BaseModel):
    id: str
    type: ArtifactType
    language: Optional[str] = None
    tags: List[Tag] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SpeechAnalysisRequest(BaseModel):
    type: Literal[ArtifactType.SPEECH] = 'speech'
    transcript: str = Field(min_length=1)
    language: str = "en"

    @field_validator('transcript')
    @classmethod
    def transcript_must_not_be_empty_whitespace(cls, v):
        if not v.strip():
            raise ValueError('Transcript must not be empty whiutespace')
        return v.strip().lower()
    
class ImageAnalysisRequest(BaseModel):
    type: Literal[ArtifactType.IMAGE] = 'image'
    image_url: HttpUrl
    language: str = "en"

class ArtifactResponse(BaseModel):
    items: List[Artifact] = []

class TagSummary(BaseModel):
    value: str
    category: TagCategory
    count: int

class TagSummaryResponse(BaseModel):
    items: List[TagSummary] = []

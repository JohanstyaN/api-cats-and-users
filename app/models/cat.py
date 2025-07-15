from typing import Optional
from pydantic import BaseModel

class Weight(BaseModel):
    imperial: Optional[str] = None
    metric: Optional[str]   = None

class ImageData(BaseModel):
    id:     Optional[str]   = None
    width:  Optional[int]   = None
    height: Optional[int]   = None
    url:    Optional[str]   = None

class Breed(BaseModel):
    id:                 str
    name:               Optional[str]       = None
    origin:             Optional[str]       = None
    temperament:        Optional[str]       = None
    life_span:          Optional[str]       = None
    description:        Optional[str]       = None
    reference_image_id: Optional[str]       = None
    vetstreet_url:      Optional[str]       = None
    wikipedia_url:      Optional[str]       = None
    country_codes:      Optional[str]       = None
    country_code:       Optional[str]       = None
    
    indoor:             Optional[int]       = None
    alt_names:          Optional[str]       = None
    adaptability:       Optional[int]       = None
    affection_level:    Optional[int]       = None
    child_friendly:     Optional[int]       = None
    dog_friendly:       Optional[int]       = None
    energy_level:       Optional[int]       = None
    grooming:           Optional[int]       = None
    health_issues:      Optional[int]       = None
    intelligence:       Optional[int]       = None
    shedding_level:     Optional[int]       = None
    social_needs:       Optional[int]       = None
    stranger_friendly:  Optional[int]       = None
    vocalisation:       Optional[int]       = None
    experimental:       Optional[int]       = None
    hairless:           Optional[int]       = None
    natural:            Optional[int]       = None
    rare:               Optional[int]       = None
    rex:                Optional[int]       = None
    suppressed_tail:    Optional[int]       = None
    short_legs:         Optional[int]       = None
    hypoallergenic:     Optional[int]       = None

    weight:             Optional[Weight]    = None
    image:              Optional[ImageData] = None

    class Config:
        extra = "ignore"
        orm_mode = True

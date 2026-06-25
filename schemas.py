from pydantic import BaseModel, Field
from datetime import datetime


class TourCreateSchema(BaseModel):
    title: str = Field(examples=["Tour to the Carpathians"])
    country: str = Field(examples=["Ukraine"])
    price: float = Field(ge=1)
    duration_days: int = Field(ge=1)


class TourSavedSchema(TourCreateSchema):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
from pydantic import BaseModel


class PropertyInput(BaseModel):
    model: str
    area: float
    district: str
    city: str
    number_of_rooms: int
    floor: str
    type_of_market: str
    parking: bool
    elevator: bool
    year_of_creation: int
    internet: bool
    type_of_building: str
    basement: bool
    balcony: bool
    garden: bool
    terrace: bool

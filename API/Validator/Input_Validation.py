from pydantic import BaseModel,Field,computed_field
from typing import  Annotated,Literal

class predict_IP_validation(BaseModel):
    property_Type:Annotated[Literal["flat","house"],Field(...,description="please select the valid property type")]
    bedRooms:Annotated[float,Field(...,description="no of bedrooms",ge=1)]
    bathrooms:Annotated[int,Field(...,description="no of bathrooms",ge=1)]
    balconies:Annotated[str,Field(...,description="no of balconies")]
    built_up_area:Annotated[float,Field(...,description="built up area",gt=100.00)]
    sector:Annotated[str,Field(...,description="sector number")]
    servent_room:Annotated[int,Field(...,description="servent room")]
    floor_category:Annotated[str,Field(...,description="floor_category")]
    store_room:Annotated[int,Field(...,description="store room")]
    @computed_field
    @property
    def area_per_bedroom(self)-> float:
        return round((self.built_up_area)/(self.bedRooms),2)






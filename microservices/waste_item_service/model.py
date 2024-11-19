from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr

from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class WasteItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    category: str = Field(...)
    sorting_instructions: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Expired Food",
                "category": "Food Waste",
                "sorting_instructions": "dawdawda",
            }
        },
    )


class UpdateWasteItemModel(BaseModel):
    name: str = Field(...)
    category: str = Field(...)
    sorting_instructions: str = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Expired Food",
                "category": "Food Waste",
                "sorting_instructions": "dawdadwada",
            }
        },
    )


class WasteItemCollection(BaseModel):
    waste_items: List[WasteItemModel]


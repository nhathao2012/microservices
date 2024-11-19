from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId


PyObjectId = Annotated[str, BeforeValidator(str)]

class ItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    category: str
    sorting_instructions: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Apple Core",
                "category": "Food waste",
                "description": "The core of an apple.",
                "disposal_guidelines": "Compost if possible.",
            }
        },
    )

class WasteCategoryModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    category: str = Field(...)
    description: str = Field(...)
    disposal_guidelines: str = Field(...)
    #items: List[ItemModel] = []
    items: List[ItemModel] = Field(default_factory=list)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "category": "Food waste",
                "description": "Food waste",
                "disposal_guidelines": "How to dispose",
                "items": [
                    {
                        "name": "Apple Core",
                        "category": "Food waste",
                        "description": "The core of an apple.",
                        "disposal_guidelines": "Compost if possible."
                    }
                ]
            }
        },
    )


class UpdateWasteCategoryModel(BaseModel):
    category: str = Field(...)
    description: str = Field(...)
    disposal_guidelines: str = Field(...)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "category": "Food waste",
                "description": "Food waste",
                "disposal_guidelines": "How to dispose",
            }
        },
    )


class WasteCategoryCollection(BaseModel):
    waste_categories: List[WasteCategoryModel]

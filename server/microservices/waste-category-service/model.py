from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr

from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from bson import ObjectId

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class WasteCategoryModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    category: str = Field(...)
    description: str = Field(...)
    disposal_guidelines: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "category": "Food waste",
                "description": "Food waste",
                "disposal_guidelines": "How to dispose",
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


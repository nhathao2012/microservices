from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr

from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from bson import ObjectId

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class ChallengeModel(BaseModel):
    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    category: str = Field(...)
    description: str = Field(...)
    difficulty_level: int = Field(..., le=10)
    scoring_criteria: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "category": "Food waste",
                "description": "expired food",
                "difficulty_level (number/10)": "2",
                "scoring_criteria": "a lot of food are wasting",
            }
        },
    )


class UpdateChallengeModel(BaseModel):
    category: str = Field(...)
    description: str = Field(...)
    difficulty_level: int = Field(..., le=10)
    scoring_criteria: str = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "category": "Food waste",
                "description": "expired food",
                "difficulty_level": "2",
                "scoring_criteria": "a lot of food are wasting",
            }
        },
    )


class ChallengeCollection(BaseModel):
    challenges: List[ChallengeModel]


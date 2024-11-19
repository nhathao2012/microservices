from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr

from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

from bson import ObjectId

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    age: int = Field(..., le=100)
    email: EmailStr = Field(...)
    password: str = Field(...)
    course: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "age": "18",
                "email": "jdoe@example.com",
                "password": "YOURPASSWORD",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
            }
        },
    )


class UpdateUserModel(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    course: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "age": "18",
                "email": "jdoe@example.com",
                "password": "YOUR PASSWORD",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
            }
        },
    )


class UserCollection(BaseModel):
    users: List[UserModel]


class LoginModel(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "email": "jdoe@example.com",
                "password": "123456",
            }
        },
    )


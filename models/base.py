from typing import Annotated

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, PlainSerializer

PyObjectId = Annotated[
    ObjectId,
    PlainSerializer(
        lambda s: str(s),  # pylint: disable=unnecessary-lambda
        return_type=str,
        when_used="json",
    ),
]


class MongoBaseModel(BaseModel):
    # NOTE: ObjectIds store the creation time of the object
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    model_config = ConfigDict(
        extra="allow",  # NOTE: be careful with this, disable when correcting attributes
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

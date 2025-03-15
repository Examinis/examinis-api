from pydantic import BaseModel, ConfigDict


class UserStatusSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class UserStatusCreateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str


class UserStatusUpdateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str

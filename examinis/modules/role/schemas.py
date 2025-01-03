from pydantic import BaseModel, ConfigDict


class RoleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class RoleCreateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str


class RoleUpdateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, conint


class PageParams(BaseModel):
    """ Request query params for paginated API. """
    page: conint(ge=1) = 1
    size: conint(ge=1, le=100) = 10
    order_by: Optional[str] = None
    order_desc: bool = False


T = TypeVar("T")


class PagedResponseSchema(BaseModel, Generic[T]):
    """Response schema for any paged API."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    total: int
    page: int
    size: int
    results: List[T]

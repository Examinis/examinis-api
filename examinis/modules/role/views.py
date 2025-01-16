from typing import List

from fastapi import APIRouter, Depends

from examinis.modules.role.schemas import RoleSchema
from examinis.modules.role.service import RoleService

router = APIRouter(
    prefix='/role',
    tags=['role'],
)


@router.get('/', response_model=List[RoleSchema])
def get_all(role_service: RoleService = Depends(RoleService)):
    return role_service.get_all()


@router.get('/{role_id}', response_model=RoleSchema)
def get_by_id(role_id: int, role_service: RoleService = Depends(RoleService)):
    return role_service.get(role_id)

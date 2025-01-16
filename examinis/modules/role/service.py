from fastapi import Depends, HTTPException

from examinis.core.ServiceAbstract import ServiceAbstract
from examinis.models.role import Role
from examinis.modules.role.repository import RoleRepository


class RoleService(ServiceAbstract[Role]):
    def __init__(self, repository: RoleRepository = Depends(RoleRepository)):
        super().__init__(repository)

    def get(self, id: int) -> Role:
        role = self.repository.get(id)

        if not role:
            raise HTTPException(status_code=404, detail='Role not found')

        return role

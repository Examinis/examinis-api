from http import HTTPStatus
from pathlib import Path
import shutil

from fastapi import Depends, HTTPException, UploadFile

from examinis.common.validators.identity_proof_validator import PDFUploadValidation
from examinis.core.security import hash_password
from examinis.core.service_abstract import ServiceAbstract
from examinis.models.user import User
from examinis.modules.role.role_enum import RoleEnum
from examinis.modules.user.repository import UserRepository
from examinis.modules.user_status.user_status_enum import UserStatusEnum


class UserService(ServiceAbstract[User]):
    def __init__(
        self,
        repository: UserRepository = Depends(UserRepository),
    ):
        super().__init__(repository)
        self.repository = repository

    async def create(self, user: dict, identity_proof: UploadFile) -> User:
        if self.repository.get_by_email(user['email']):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='User with this email already exists',
            )

        user['password'] = hash_password(user['password'])
        user['role_id'] = RoleEnum.PROFESSOR.value
        user['status_id'] = UserStatusEnum.PENDING.value

        self._save_identity_proof(user, identity_proof)

        return super().create(user)

    def _save_identity_proof(self, user: dict, identity_proof: UploadFile) -> User:
        PDFUploadValidation.validate_pdf(identity_proof)

        upload_dir = Path("uploads/users/identity_proofs")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / f"{user['email']}.pdf"

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(identity_proof.file, buffer)

        user['identity_proof'] = str(file_path)
    
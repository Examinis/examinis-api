from typing import List
from fastapi import Depends

from examinis.common.schemas.pagination_schema import PageParams
from examinis.core.RepositoryAbstract import RepositoryAbstract, Session
from examinis.db.config import get_session
from examinis.models import Exam
from examinis.modules.exam.schemas import ExamPageParams


class ExamRepository(RepositoryAbstract[Exam]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(Exam, session=session)

    def create_manual(self, exam: dict, questions: list) -> Exam:
        exam_db = self.create(exam)
        exam_db.questions = questions
        self.session.commit()
        return exam_db

    def create_automatic(self, exam: dict, questions: list) -> Exam:
        exam_db = self.create(exam)
        exam_db.questions = questions
        self.session.commit()
        return exam_db

    def get_all_paginated(self, params: ExamPageParams) -> List[Exam]:
        query = self.session.query(Exam)

        if params.subject_id:
            query = query.filter(Exam.subject_id == params.subject_id)

        if params.user_id:
            query = query.filter(Exam.user_id == params.user_id)

        params_dict = params.model_dump(exclude={'subject_id', 'user_id'})

        return super().get_all_paginated(query=query, params= params_dict)
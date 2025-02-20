from typing import List

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from examinis.core.RepositoryAbstract import RepositoryAbstract
from examinis.db.config import get_session
from examinis.models import Question
from examinis.modules.question.schemas import QuestionPageParams


class QuestionRepository(RepositoryAbstract[Question]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(Question, session=session)

    def get_by_list(self, question_ids: List[int]) -> List[Question]:
        return (
            self.session.query(Question)
            .filter(Question.id.in_(question_ids))
            .all()
        )

    def get_random_by_subject(
        self, subject_id: int, amount: int
    ) -> List[Question]:
        return (
            self.session.query(Question)
            .filter(Question.subject_id == subject_id)
            .order_by(func.random())
            .limit(amount)
            .all()
        )
    
    def get_all_paginated(self, params: QuestionPageParams) -> List[Question]:
        query = self.session.query(Question)

        if params.subject_id:
            query = query.filter(Question.subject_id == params.subject_id)
        
        if params.difficulty_id:
            query= query.filter(Question.difficulty_id == params.difficulty_id)

        query = query.options(joinedload(Question.difficulty))

        return super().get_all_paginated(query=query, params=params)

    def count_filtered(self, params: QuestionPageParams) -> int:
        query = self.session.query(func.count(Question.id))

        if params.subject_id:
            query = query.filter(Question.subject_id == params.subject_id)
        
        if params.difficulty_id:
            query.query.filter(Question.difficulty_id == params.difficulty_id)

        return query.scalar()


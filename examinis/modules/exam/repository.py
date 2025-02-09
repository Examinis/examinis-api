from fastapi import Depends

from examinis.core.RepositoryAbstract import RepositoryAbstract, Session
from examinis.db.config import get_session
from examinis.models import Exam


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

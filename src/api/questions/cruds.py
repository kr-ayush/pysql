"""
CRUDs for Question Table
"""

from typing import List
from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from database.models import Questions
from api.questions.schemas import QuestionPayload


class QuestionsService:
    """cruds for Question"""

    def __init__(self, db: Session):
        self.db = db

    def get_all_questions(self):
        """get all questions"""
        return self.db.query(
            Questions.question_id,
            Questions.question,
            Questions.difficulty,
            Questions.tags,
        ).all()

    def get_questions(self, question_id: int):
        """get question by id"""
        return (
            self.db.query(
                Questions.question_id,
                Questions.question,
                Questions.difficulty,
                Questions.tags,
            )
            .filter(Questions.question_id == question_id)
            .first()
        )

    def create_questions(self, raw_data: List[QuestionPayload]):
        """create entries in db"""
        obj_lst = []
        for data in raw_data:
            obj_lst.append(
                Questions(
                    question=data.question,
                    solution=data.solution,
                    difficulty=data.difficulty,
                    hints=data.hints,
                    tags=data.tags,
                )
            )
        self.db.add_all(obj_lst)
        self.db.commit()
        return True

    def update_questions(self, questions_id: int, raw_data: QuestionPayload):
        """update questions in db"""
        self.db.execute(
            update(Questions)
            .where(Questions.question_id == questions_id)
            .values(**raw_data.__dict__)
        )
        self.db.commit()
        return True

    def delete_questions(self, questions_id: int):
        """delete questios in db"""
        self.db.execute(
            delete(Questions).where(Questions.question_id == questions_id)
        )
        self.db.commit()
        return True

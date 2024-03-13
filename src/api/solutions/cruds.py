"""
CRUDs for Solutions Table
"""

from sqlalchemy import text
from sqlalchemy.orm import Session
from database.models import Questions


class SolutionsService:
    """Cruds for Solutions"""

    def __init__(self, db: Session):
        self.db = db

    def get_all_solutions(self):
        """get all solutions for questions"""
        return self.db.query(Questions.question_id, Questions.solution).all()

    def get_solution_by_id(self, question_id: int):
        """get solutions of the question"""
        return (
            self.db.query(Questions.solution)
            .filter(Questions.question_id == question_id)
            .first()
        )

    def get_hints(self, question_id: int):
        """get hints of the questions"""
        return (
            self.db.query(Questions.hints)
            .filter(Questions.question_id == question_id)
            .first()
        )


class SolutionStmt:

    @staticmethod
    def stmt_create_dummy_table(tablename: str):
        return text(
            f"CREATE TABLE test_{tablename} AS SELECT * FROM {tablename};"
        )

    @staticmethod
    def stmt_drop_dummy_table(tablename: str):
        return text(f"DROP TABLE IF EXISTS test_{tablename};")

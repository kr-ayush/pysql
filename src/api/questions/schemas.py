"""
Pydantic Model
"""

from typing import List
from pydantic import BaseModel


class QuestionPayload(BaseModel):
    """Pydanctic model for Question Table"""

    question: str
    solution: str
    difficulty: str = "Easy"
    hints: str
    tags: str


class RequestQuestionModel(BaseModel):
    """Pydantic Model for Question API"""

    payload: List[QuestionPayload]

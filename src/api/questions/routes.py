"""
Routes for Question
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from database.db import get_db
from api.questions import cruds
from api.questions import schemas

router = APIRouter()


@router.get("/")
def route_get_questions(
    question_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Endpoint: Get All Questions or specific question based on Id
    Args:
        question_id Optional[int]: Primary Key of entries in question table
        db (Session): DB Session of SQLAlchemy
    Returns:
        ORJSONResponse
    """
    keys = ["question_id", "question", "difficulty", "hints"]
    if question_id:
        result = cruds.QuestionsService(db).get_questions(
            question_id=question_id
        )
        if result:
            return ORJSONResponse(
                content=jsonable_encoder(dict(zip(keys, result))),
                status_code=200,
            )
        raise HTTPException(detail="Question not Found", status_code=404)
    result = cruds.QuestionsService(db).get_all_questions()
    result = [dict(zip(keys, res)) for res in result]
    if result:
        return ORJSONResponse(
            content=jsonable_encoder(result), status_code=200
        )
    raise HTTPException(detail="Question not Found", status_code=404)


@router.post("/")
def route_post_question(
    payload: schemas.RequestQuestionModel,
    db: Session = Depends(get_db),
):
    """Endpoint: POST Question in Table
    Args:
        payload (RequestQuestionModel): Pydantic Model
        db (Session): DB Session of SQLAlchemy
    Returns:
        ORJSONResponse
    """
    result = cruds.QuestionsService(db).create_questions(
        raw_data=payload.payload
    )
    if result:
        return ORJSONResponse(content="Questions Created", status_code=201)
    raise HTTPException(detail=result, status_code=400)


@router.patch("/")
def route_patch_question(
    question_id: int,
    payload: schemas.QuestionPayload,
    db: Session = Depends(get_db),
):
    """Endpoint: Patch Question in Table
    Args:
        question_id (int): Question ID
        payload (RequestQuestionModel): Pydantic Model
        db (Session): DB Session of SQLAlchemy
    Returns:
        ORJSONResponse
    """
    result = cruds.QuestionsService(db).update_questions(
        questions_id=question_id, raw_data=payload
    )
    if result:
        return ORJSONResponse(content="Questions Updated", status_code=200)
    raise HTTPException(detail=result, status_code=400)


@router.delete("/")
def route_delete_question(question_id: int, db: Session = Depends(get_db)):
    """Endpoint: POST Question in Table
    Args:
        question_id (int): Question Id
        db (Session): DB Session of SQLAlchemy
    Returns:
        ORJSONResponse
    """
    result = cruds.QuestionsService(db).delete_questions(
        questions_id=question_id
    )
    if result:
        return ORJSONResponse(content="Questions Deleted", status_code=200)
    raise HTTPException(detail=result, status_code=400)

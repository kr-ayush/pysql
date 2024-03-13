"""
Routes.py
"""

import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from api.solutions import cruds
from api.solutions import schemas
from database.db import get_db
from database.models import TableName
from utils.solutions import SolutionGenerator

router = APIRouter()


@router.get("/hint/{question_id}")
def route_get_hints(question_id: int, db: Session = Depends(get_db)):
    """Endpoint: Get Hints for Provided Question
    Args:
        question_id (int): Question Id
        db (Session): SQLAlchemy Session
    Returns:
        ORJSONResponse
    """
    results = cruds.SolutionsService(db).get_hints(question_id=question_id)
    if results:
        return ORJSONResponse(
            content=jsonable_encoder({"hints": results[0]}), status_code=200
        )
    raise HTTPException(status_code=404, detail="Question Id not Found")


@router.get("/soln/{question_id}")
def route_get_solutions(question_id: int, db: Session = Depends(get_db)):
    """Endpoint: Get Hints for Provided Question
    Args:
        question_id (int): Question Id
        db (Session): SQLAlchemy Session
    Returns:
        ORJSONResponse
    """
    results = cruds.SolutionsService(db).get_solution_by_id(
        question_id=question_id
    )
    if results:
        return ORJSONResponse(
            content=jsonable_encoder({"solutions": results[0]}),
            status_code=200,
        )
    raise HTTPException(status_code=404, detail="Question Id not Found")


@router.post("/{question_id}")
def route_check_solution(
    question_id: int, data: schemas.RequestSoln, db: Session = Depends(get_db)
):
    """Endpoint: Accept User Solutions
    Args:
        question_id (int): Question Id
        query (RequestSoln)
        db (Session): SQLAlchemy Session
    Returns:
        ORJSONResponse
    """
    try:
        tables = TableName.hospital
        soln = SolutionGenerator.response[question_id]
        query = data.query
        tablename = set(tables).intersection(set(query.split(" ")))
        if not tablename:
            raise HTTPException("Table Name not Passed Correctly", 200)
        with db.begin():
            for table in tablename:
                if table.endswith(";"):
                    table = table.split(";")[0]
                db.execute(
                    cruds.SolutionStmt.stmt_create_dummy_table(tablename=table)
                )
                query = query.replace(table, f"test_{table}")
            stmt = text(query)
            result = db.execute(stmt)
            if not result.returns_rows or soln is None:
                return ORJSONResponse(
                    {
                        "flag": "Failed",
                        "message": "output does not match",
                        "result": soln.to_dict(orient="records"),
                    },
                    200,
                )
            df = pd.DataFrame(result.fetchall())
            df.columns = result.keys()
            try:
                flag_compare_result = df.compare(soln)
            except Exception:
                return ORJSONResponse(
                    {
                        "flag": "Failed",
                        "message": "Output does not match",
                        "output": df.to_dict(orient="records"),
                        "solution": soln.to_dict(orient="records"),
                    },
                    200,
                )
            if flag_compare_result.empty:
                return ORJSONResponse(
                    {
                        "flag": "Passed",
                        "message": "Output Matched",
                        "result": df.to_dict(orient="records"),
                        "solution": soln.to_dict(orient="records"),
                    },
                    200,
                )
            else:
                return ORJSONResponse(
                    {
                        "flag": "Failed",
                        "message": "Output does not match",
                        "result": df.to_dict(orient="records"),
                    },
                    200,
                )
    except HTTPException as err:
        raise HTTPException(
            detail=str(err.with_traceback),
            status_code=err.status_code,
        ) from err
    finally:
        for table in tablename:
            if table.endswith(";"):
                table = table.split(";")[0]
            db.execute(
                cruds.SolutionStmt.stmt_drop_dummy_table(tablename=table)
            )

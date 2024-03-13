"""
Router File
"""

from fastapi import APIRouter
from api.questions.routes import router as ques_router
from api.solutions.routes import router as solu_router

router = APIRouter()
router.include_router(ques_router, prefix="/questions", tags=["questions"])
router.include_router(solu_router, prefix="/solutions", tags=["solutions"])

"""
Pydanctic Models
"""

from pydantic import BaseModel


class RequestSoln(BaseModel):
    query: str

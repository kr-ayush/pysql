"""
Solutions Utils
"""

import pandas as pd
from sqlalchemy import text
from utils import Singleton
from api.solutions import cruds
from database.db import get_db


class SolutionGenerator(metaclass=Singleton):

    response = {}

    async def generate_solutions_bank(self):
        """Generate Solutions for all Question"""
        db = next(get_db())
        results = cruds.SolutionsService(db).get_all_solutions()
        if results is None:
            raise Exception
        for res in results:
            stmt = text(res[1])
            soln = db.execute(stmt)
            df = pd.DataFrame(soln.fetchall())
            df.columns = soln.keys()
            self.response[res[0]] = df
        db.close()

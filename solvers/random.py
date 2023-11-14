from typing import List
from models import SolverABC
from models import Request

class RandomSolver(SolverABC):
    def solve(r: Request) -> List[int]:
        return super().solve()
    
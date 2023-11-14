from typing import List
from models import SolverABC
from models import Request

def SimpleSolver(SolverABC):
    def solve(r: Request) -> List[int]:
        epoints = sorted(enumerate(r.points), key=lambda x: x[1].priority)
        acc = 0
        time_left
        for i, point in epoints:

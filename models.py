"""
Contains described models.
"""

from typing import List
import abc
import json
import dataclasses


@dataclasses.dataclass
class Coordinates:
    lat: float
    lon: float

    def __add__(self, coord: "Coordinates") -> "Coordinates":
        return Coordinates(self.lat + coord.lat, self.lon + coord.lon)

    def __sub__(self, coord: "Coordinates") -> "Coordinates":
        return Coordinates(self.lat - coord.lat, self.lon - coord.lon)

    def __mul__(self, m):
        return Coordinates(self.lat * m, self.lon * m)

    def __truediv__(self, d):
        return Coordinates(self.lat / d, self.lon / d)

    def __iter__(self):
        return iter((self.lat, self.lon))


@dataclasses.dataclass
class RequestPoint:
    priority: int
    position: Coordinates

    @classmethod
    def from_dict(cls, data: dict) -> "RequestPoint":
        return cls(priority=data["priority"], position=Coordinates(*data["position"]))


@dataclasses.dataclass
class Request:
    capacity: int
    time_left: int
    penalty: int
    points: List[RequestPoint]
    time_matrix: List[List[int]]

    @property
    def points_number(self) -> int:
        return len(self.points)

    @property
    def scooter_number(self) -> int:
        return self.points_number - 1

    @property
    def center(self) -> Coordinates:
        return (
            sum([p.position for p in self.points], start=Coordinates(0, 0))
            / self.points_number
        )

    def move(self, delta: Coordinates):
        for p in self.points:
            p.position -= delta

    def delta(self, coord: Coordinates) -> Coordinates:
        return self.center - coord

    @property
    def priorities(self) -> List[int]:
        return [p.priority for p in self.points]

    @classmethod
    def from_dict(cls, data: dict) -> "Request":
        return cls(
            capacity=int(data["capacity"]),
            time_left=int(data["time_left"]),
            penalty=int(data["penalty"]),
            points=[RequestPoint.from_dict(p) for p in data["points"]],
            time_matrix=data["time_matrix"],
        )

    def cost(self, itenerary: List[int]) -> int:
        # return sum([for zip()])
        pass

    @classmethod
    def from_file(cls, path: str) -> "Request":
        with open(path, "r") as f:
            return cls.from_dict(json.load(f))


class SolverABC(abc.ABC):
    @abc.abstractmethod
    def solve(r: Request) -> List[int]:
        pass

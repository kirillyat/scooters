"""
Contains described models.
"""

from typing import List
import numpy as np
import abc
import json
import dataclasses


@dataclasses.dataclass
class Coordinates:
    """
    Сласс координаты
    Attributes:
       lon: Долгота.
       lat: Широта.
    """

    lon: float
    lat: float

    def __add__(self, coord: "Coordinates") -> "Coordinates":
        return Coordinates(self.lon + coord.lon, self.lat + coord.lat)

    def __sub__(self, coord: "Coordinates") -> "Coordinates":
        return Coordinates(self.lon - coord.lon, self.lat - coord.lat)

    def __mul__(self, m):
        return Coordinates(self.lon * m, self.lat * m)

    def __truediv__(self, d):
        return Coordinates(self.lon / d, self.lat / d)

    def __iter__(self):
       return iter((self.lon, self.lat))


@dataclasses.dataclass
class Scooter(Coordinates):
    """
    Attributes:
        lat: Широта.
        lon: Долгота.
        priority: Приоритет самоката.
    """

    priority: int

    @classmethod
    def from_(cls, x=0, y=0, p=0):
        return cls(lat=x, lon=y, priority=p)

    @classmethod
    def from_dict(cls, data: dict) -> "Scooter":
        return cls(priority=data["priority"], position=Coordinates(*data["position"]))


@dataclasses.dataclass
class Request:
    """
    Класс для обработки данных.

    Attributes:
        capacity: Допустимое количество точек в маршруте.
        penalty: Штраф за одну минуту маршрута.
        scooters: Координаты и приоритет самокатов.
        time: Допустимая продолжительность маршрута.
        time_matrix: Матрица временных затрат на перемещение между точками.
    """

    capacity: int
    penalty: int
    scooters: List[Scooter]
    time: int
    time_matrix: List[List[int]]

    @property
    def points_number(self) -> int:
        return len(self.scooters)

    @property
    def scooter_number(self) -> int:
        return self.points_number - 1

    @property
    def M(self) -> int:
        return self.time_matrix

    def move(self, delta: Coordinates):
        for p in self.scooters:
            p += delta

    def move_to(self, new_center: Coordinates):
        delta = self.center - new_center
        for scooter in self.scooters:
            scooter.lat -= delta.lat
            scooter.lon -= delta.lon

    @property
    def center(self) -> Coordinates:
        return sum(
            (scooter for scooter in self.scooters), start=Scooter(0, 0, 0)
        ) / len(self.scooters)

    def delta(self, coord: Coordinates) -> Coordinates:
        return self.center - coord

    @property
    def priorities(self) -> np.array:
        return np.array([s.priority for s in self.scooters])

    @classmethod
    def from_dict(cls, data: dict) -> "Request":
        return cls(
            capacity=int(data["capacity"]),
            penalty=int(data["penalty"]),
            scooters=[Scooter.from_dict(p) for p in data["points"]],
            time=int(
                data["time_left"]
            ),  # FIXME: Возможно изменение контракта time_left -> time
            time_matrix=np.array(data["time_matrix"]),
        )

    def check(self, itenerary: List[int]) -> bool:
        """
        Маршрут должен быть.
            - длиной менее чем capacity
            - продолжительностью по времени менее чем time
        Args:
            itenerary: Номера вершин(самокатов) в порядке их посещения.
        """
        # TODO: Уточтинить нужно ли чтобы маршрут начинался и заканчивался в нулевой точке

        if len(itenerary) - 2 > self.capacity:
            return False
        return self.cost(itenerary) <= self.time

    def scores(self, iteneraries: List[List[int]]) -> List[float]:
        return [self.score(itenerary) for itenerary in iteneraries]

    def costs(self, iteneraries: List[List[int]]) -> List[float]:
        return [self.cost(itenerary) for itenerary in iteneraries]

    def cost(self, itenerary: List[int]) -> float:
        prev = 0
        cost = 0
        for i in itenerary:
            cost += self.time_matrix[prev][i]
            prev = i
        return cost

    def score(self, itenerary: List[int]) -> float:
        """
        Подсчет стоимости маршрута.
        Args:
            itenerary: Номера вершин(самокатов) в порядке их посещения.
        """
        # TODO: Уточтинить нужно ли чтобы маршрут начинался и заканчивался в нулевой точке
        cost = 0
        prev = 0
        for i in itenerary:
            cost += self.scooters[i].priority
            cost -= self.time_matrix[prev][i] * self.penalty
            prev = i
        return cost

    @classmethod
    def from_json(cls, path: str) -> "Request":
        with open(path, "r") as f:
            return cls.from_dict(json.load(f))

    @classmethod
    def from_txt(cls, path: str) -> "Request":
        with open(path, "r") as f:
            n = int(f.readline().strip())
            scooters = []
            for _ in range(n + 1):
                line = f.readline().strip().split()
                scooters.append(Scooter(*map(float, line[:2:]), int(line[2])))

            time_matrix = [
                list(map(int, f.readline().strip().split())) for _ in range(n + 1)
            ]
            capacity = int(f.readline().strip())
            time = int(f.readline().strip())
            penalty = float(f.readline().strip())
            return cls(
                capacity=capacity,
                penalty=penalty,
                scooters=scooters,
                time=time,
                time_matrix=time_matrix,
            )


class SolverABC(abc.ABC):
    @abc.abstractmethod
    def solve(r: Request) -> List[int]:
        pass


from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import numpy as np
import json
from typing import List

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
class Scooter(Coordinates):
    priority: int

    @classmethod
    def from_dict(cls, data: dict) -> "Scooter":
        return cls(priority=data["priority"], lat=data["position"][0], lon=data["position"][1])


@dataclasses.dataclass
class Request:
    capacity: int
    penalty: int
    scooters: List[Scooter]
    time: int
    time_matrix: List[List[int]]

    @classmethod
    def from_dict(cls, data: dict) -> "Request":
        return cls(
            capacity=int(data["capacity"]),
            penalty=int(data["penalty"]),
            scooters=[Scooter.from_dict(p) for p in data["points"]],
            time=int(data["time_left"]),
            time_matrix=np.array(data["time_matrix"]),
        )

    def cost(self, itinerary: List[int]) -> float:
        prev = 0
        cost = 0
        for i in itinerary:
            cost += self.time_matrix[prev][i]
            prev = i
        return cost


def create_data_model(request: Request):
    """Stores the data for the problem."""
    data = {}
    data['time_matrix'] = request.time_matrix
    data['num_vehicles'] = num_couriers
    data['depot'] = 0
    return data

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    routes = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route_distance = 0
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        route.append(manager.IndexToNode(index))
        routes.append(route)
        total_distance += route_distance
    return routes

def solve_vrp(request: Request, num_couriers: int):
    data = create_data_model(request)
    
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time constraint.
    dimension_name = 'Time'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        request.time,  # vehicle maximum travel time
        True,  # start cumul to zero
        dimension_name)
    time_dimension = routing.GetDimensionOrDie(dimension_name)
    time_dimension.SetGlobalSpanCostCoefficient(100)

    # Set the search parameters.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 30

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        routes = print_solution(data, manager, routing, solution)
        return routes
    else:
        print('No solution found !')
        return []

# Example usage
request_data = {
    "capacity": 4,
    "penalty": 1,
    "points": [
        {"priority": 0, "position": [0, 0]},
        {"priority": 10, "position": [1, 0]},
        {"priority": 20, "position": [2, 0]},
        {"priority": 30, "position": [3, 0]},
        {"priority": 40, "position": [4, 0]}
    ],
    "time_left": 100,
    "time_matrix": [
        [0, 1, 2, 3, 4],
        [1, 0, 1, 2, 3],
        [2, 1, 0, 1, 2],
        [3, 2, 1, 0, 1],
        [4, 3, 2, 1, 0]
    ]
}

request = Request.from_dict(request_data)
num_couriers = 2
routes = solve_vrp(request, num_couriers)
print("Routes:", routes)

import folium
from typing import List
from typing import Optional
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from src.models import Request


def GeoMap(r: Request, route: Optional[List[int]] = None, rote_only: bool = False) -> folium.Map:
    M = folium.Map(location=list(r.center), zoom_start=11)

    for i, point in enumerate(r.scooters):
        if i == 0:
            color = "darkred"
        elif route and i in route:
            color = "green"
        else:
            color = "blue"
        if not rote_only or i in route:
            folium.Marker(
                location=[point.lat, point.lon],
                icon=folium.Icon(icon="star", color=color),
            ).add_to(M)
    if route:
        folium.PolyLine(
            locations=[list(r.scooters[i]) for i in route],
            color="red",
            weight=15,
            opacity=0.8,
        ).add_to(M)

    return M


def Graph(r: Request, rote: Optional[List[int]]):
    # TODO: graph visualization
    G = nx.Graph()

    for i in range(r.scooter_number):
        G.add_node(i)
    for i in range(r.scooter_number):
        for j in range(i + 1, r.scooter_number):
            # G.add_edge(i, j, weight=r.time_matrix[i][j])
            G.add_edge(i, j)
    return G

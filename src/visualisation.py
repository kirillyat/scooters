import folium
from typing import List
from typing import Optional
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import itertools


from src.models import Request


def GeoMap(
    r: Request, route: Optional[List[int]] = None, rote_only: bool = True
) -> folium.Map:
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


def get_color_palette(num_colors: int) -> List[str]:
    colors = plt.get_cmap("tab20", num_colors).colors
    return [matplotlib.colors.rgb2hex(color) for color in colors]


colours = [
    "darkpurple",
    "red",
    "lightgray",
    "darkblue",
    "cadetblue",
    "gray",
    "beige",
    "blue",
    "black",
    "lightred",
    "darkred",
    "pink",
    "orange",
    "green",
    "lightblue",
    "white",
    "purple",
    "darkgreen",
    "lightgreen",
]


def GeoMap_Routes(
    r: Request, routes: List[List[int]] = None, rote_only: bool = False
) -> folium.Map:
    M = folium.Map(location=list(r.center), zoom_start=11)
    route_colors = get_color_palette(len(routes)) if routes else []
    for route, color_route, color in zip(routes, itertools.cycle(route_colors), itertools.cycle(colours)
):
        folium.PolyLine(
            locations=[[r.scooters[i].lat, r.scooters[i].lon] for i in route],
            color=color_route,
            weight=15,
            opacity=0.8,
        ).add_to(M)
        for i in route:
            folium.Marker(
                location=[r.scooters[i].lat, r.scooters[i].lon],
                icon=folium.Icon(icon="star", color=color),
            ).add_to(M)

    return M

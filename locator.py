import pandas as pd
from geopy.distance import geodesic


def calculate_distance(user_lat, user_lon, resource_lat, resource_lon):
    """Calculate distance between two locations in kilometres."""

    user_location = (user_lat, user_lon)
    resource_location = (resource_lat, resource_lon)

    distance = geodesic(
        user_location,
        resource_location
    ).kilometers

    return round(distance, 2)


def find_nearby_resources(
    resources,
    user_lat,
    user_lon,
    resource_type="All",
    max_distance=20
):
    """Find resources near the user's location."""

    results = resources.copy()

    if resource_type != "All":
        results = results[
            results["type"] == resource_type
        ]

    results["distance_km"] = results.apply(
        lambda row: calculate_distance(
            user_lat,
            user_lon,
            row["latitude"],
            row["longitude"]
        ),
        axis=1
    )

    results = results[
        results["distance_km"] <= max_distance
    ]

    results = results.sort_values(
        "distance_km"
    )

    return results
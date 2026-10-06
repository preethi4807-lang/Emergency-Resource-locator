from geopy.distance import geodesic


def calculate_distance(user_lat, user_lon, resource_lat, resource_lon):
    """
    Calculate distance between user and resource in kilometers.
    """

    user_location = (user_lat, user_lon)
    resource_location = (resource_lat, resource_lon)

    distance = geodesic(user_location, resource_location).km

    return round(distance, 2)


def find_nearest_resources(
    resources,
    user_lat,
    user_lon,
    emergency_type=None,
    max_distance=50
):
    """
    Find resources near the user and sort them by distance.
    """

    results = []

    for resource in resources:

        # Filter by emergency type if selected
        if emergency_type:

            if emergency_type == "Medical":
                allowed_types = ["Hospital", "Ambulance", "Pharmacy", "Blood Bank"]

            elif emergency_type == "Accident":
                allowed_types = ["Hospital", "Ambulance", "Police"]

            elif emergency_type == "Fire":
                allowed_types = ["Fire Station"]

            elif emergency_type == "Police":
                allowed_types = ["Police"]

            elif emergency_type == "Natural Disaster":
                allowed_types = ["Shelter", "Hospital", "Police", "Fire Station"]

            else:
                allowed_types = []

            if resource["type"] not in allowed_types:
                continue

        distance = calculate_distance(
            user_lat,
            user_lon,
            resource["latitude"],
            resource["longitude"]
        )

        if distance <= max_distance:

            resource_copy = resource.copy()
            resource_copy["distance"] = distance

            results.append(resource_copy)

    # Nearest resource first
    results.sort(key=lambda x: x["distance"])

    return results
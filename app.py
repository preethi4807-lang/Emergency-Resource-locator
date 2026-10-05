import streamlit as st
import folium

from streamlit_folium import st_folium

from database import create_database, get_resources
from locator import find_nearby_resources


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Emergency Resource Locator",
    page_icon="🚑",
    layout="wide"
)


# -----------------------------
# TITLE
# -----------------------------

st.title("🚑 Emergency Resource Locator")

st.write(
    "Find nearby hospitals, shelters and other "
    "emergency resources."
)


# -----------------------------
# CREATE DATABASE
# -----------------------------

create_database()

resources = get_resources()


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("Search Settings")

user_lat = st.sidebar.number_input(
    "Your Latitude",
    value=17.3850,
    format="%.4f"
)

user_lon = st.sidebar.number_input(
    "Your Longitude",
    value=78.4867,
    format="%.4f"
)

resource_type = st.sidebar.selectbox(
    "Resource Type",
    [
        "All",
        "Hospital",
        "Shelter",
        "Police Station",
        "Fire Station"
    ]
)

max_distance = st.sidebar.slider(
    "Maximum Distance (km)",
    min_value=1,
    max_value=50,
    value=10
)


# -----------------------------
# SEARCH BUTTON
# -----------------------------

if st.button(
    "🔍 Find Emergency Resources",
    type="primary"
):

    results = find_nearby_resources(
        resources,
        user_lat,
        user_lon,
        resource_type,
        max_distance
    )

    if results.empty:

        st.warning(
            "No emergency resources found "
            "within the selected distance."
        )

    else:

        st.success(
            f"{len(results)} resource(s) found."
        )


        # -----------------------------
        # DISPLAY RESULTS
        # -----------------------------

        st.subheader("Nearby Resources")

        for _, resource in results.iterrows():

            with st.container(border=True):

                st.write(
                    f"### {resource['name']}"
                )

                st.write(
                    f"*Type:* {resource['type']}"
                )

                st.write(
                    f"*Distance:* "
                    f"{resource['distance_km']} km"
                )

                st.write(
                    f"*Address:* "
                    f"{resource['address']}"
                )

                st.write(
                    f"*Phone:* "
                    f"{resource['phone']}"
                )


        # -----------------------------
        # MAP
        # -----------------------------

        st.subheader("🗺️ Resource Map")

        map_object = folium.Map(
            location=[
                user_lat,
                user_lon
            ],
            zoom_start=12
        )


        # User location

        folium.Marker(
            [user_lat, user_lon],
            popup="Your Location",
            tooltip="You are here",
            icon=folium.Icon(
                color="blue",
                icon="user"
            )
        ).add_to(map_object)


        # Resource markers

        for _, resource in results.iterrows():

            folium.Marker(
                [
                    resource["latitude"],
                    resource["longitude"]
                ],
                popup=(
                    f"{resource['name']}<br>"
                    f"{resource['type']}<br>"
                    f"{resource['distance_km']} km"
                ),
                tooltip=resource["name"]
            ).add_to(map_object)


        st_folium(
            map_object,
            width=1000,
            height=500
        )


# -----------------------------
# INFORMATION
# -----------------------------

st.divider()

st.info(
    "This is an academic prototype using "
    "simulated resource-location data. "
    "Always verify emergency information "
    "before relying on it in a real emergency."
)
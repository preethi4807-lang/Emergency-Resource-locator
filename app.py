import streamlit as st
import pandas as pd
import requests
import folium

from streamlit_folium import st_folium

from locator import find_nearest_resources


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Emergency Resource Locator",
    page_icon="🚨",
    layout="wide"
)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🚨 Emergency Resource Locator")

st.write(
    "Find nearby emergency resources based on your location "
    "and emergency type."
)


# ---------------------------------------------------
# LOAD RESOURCE DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("data/resources.csv")

    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    return df


resources_df = load_data()


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("📍 Emergency Search")


emergency_type = st.sidebar.selectbox(
    "Select Emergency Type",
    [
        "Medical",
        "Accident",
        "Fire",
        "Police",
        "Natural Disaster"
    ]
)


st.sidebar.subheader("Your Location")


user_lat = st.sidebar.number_input(
    "Latitude",
    value=17.3850,
    format="%.6f"
)


user_lon = st.sidebar.number_input(
    "Longitude",
    value=78.4867,
    format="%.6f"
)


max_distance = st.sidebar.slider(
    "Search Radius (km)",
    min_value=1,
    max_value=50,
    value=10
)


# ---------------------------------------------------
# EMERGENCY DESCRIPTION
# ---------------------------------------------------

st.subheader("📝 Describe the Emergency")

description = st.text_area(
    "Enter a short description",
    placeholder="Example: A road accident has occurred and someone is injured."
)


# ---------------------------------------------------
# FIND RESOURCES
# ---------------------------------------------------

if st.button("🔎 Find Emergency Resources"):

    nearest_resources = find_nearest_resources(
        resources_df.to_dict("records"),
        user_lat,
        user_lon,
        emergency_type,
        max_distance
    )

    st.session_state["nearest_resources"] = nearest_resources


# ---------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------

if "nearest_resources" in st.session_state:

    nearest_resources = st.session_state["nearest_resources"]

    st.subheader("📍 Nearby Emergency Resources")

    if len(nearest_resources) == 0:

        st.warning(
            "No emergency resources were found within the selected radius."
        )

    else:

        # ------------------------------------------------
        # SUMMARY
        # ------------------------------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Resources Found",
            len(nearest_resources)
        )

        col2.metric(
            "Nearest Distance",
            f"{nearest_resources[0]['distance']} km"
        )

        col3.metric(
            "Emergency Type",
            emergency_type
        )


        # ------------------------------------------------
        # RESOURCE CARDS
        # ------------------------------------------------

        for resource in nearest_resources:

            with st.container():

                st.markdown(
                    f"### {resource['name']}"
                )

                st.write(
                    f"**Type:** {resource['type']}"
                )

                st.write(
                    f"📍 **Distance:** "
                    f"{resource['distance']} km"
                )

                st.write(
                    f"📞 **Phone:** {resource['phone']}"
                )

                st.write(
                    f"🏠 **Address:** {resource['address']}"
                )

                st.write(
                    f"ℹ️ {resource['description']}"
                )

                st.divider()


        # ------------------------------------------------
        # MAP
        # ------------------------------------------------

        st.subheader("🗺️ Emergency Resource Map")


        map_object = folium.Map(
            location=[user_lat, user_lon],
            zoom_start=13
        )


        # User marker

        folium.Marker(
            [user_lat, user_lon],
            popup="📍 Your Location",
            tooltip="Your Location",
            icon=folium.Icon(
                color="blue",
                icon="user"
            )
        ).add_to(map_object)


        # Resource markers

        for resource in nearest_resources:

            folium.Marker(
                [
                    resource["latitude"],
                    resource["longitude"]
                ],
                popup=(
                    f"{resource['name']}<br>"
                    f"Type: {resource['type']}<br>"
                    f"Distance: {resource['distance']} km"
                ),
                tooltip=resource["name"]
            ).add_to(map_object)


        st_folium(
            map_object,
            width=1100,
            height=500
        )


# ---------------------------------------------------
# AI ASSISTANT
# ---------------------------------------------------

st.subheader("🤖 AI Emergency Assistant")

st.write(
    "The AI assistant provides general guidance about "
    "which type of emergency resource may be relevant."
)


if st.button("🤖 Analyze Emergency"):

    if description.strip() == "":

        st.warning(
            "Please describe the emergency first."
        )

    else:

        prompt = f"""
You are an emergency resource navigation assistant.

Do not diagnose medical conditions.
Do not replace emergency professionals.

Analyze the following emergency description:

{description}

Selected emergency type:
{emergency_type}

Give a short response containing:

1. Emergency category
2. Suggested resource type
3. Priority level: Low, Medium, High, or Critical
4. Short safety guidance

Keep the response concise.
"""


        try:

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )


            if response.status_code == 200:

                result = response.json()

                st.success(
                    "AI Analysis Completed"
                )

                st.write(
                    result.get("response", "No response received.")
                )

            else:

                st.error(
                    "Unable to connect to the Ollama model."
                )

        except requests.exceptions.RequestException:

            st.error(
                "Ollama is not running. Start Ollama and try again."
            )


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Emergency Resource Locator | Academic Project Prototype"
)
import streamlit as st
import numpy as np
import pandas as pd
import datetime
import requests
import pydeck as pdk

# '''
# # TaxiFareModel front
# '''

# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''

# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

# url = 'https://taxifare-126048618009.europe-west1.run.app/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''

# Layout to hold the map and inputs
st.set_page_config(layout="wide")

st.header("Taxi Fare Estimator", divider=True)

# User inputs date and time
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input('Select a date', value=datetime.date.today())

with col2:
    start_time = st.time_input('Select a time', datetime.datetime.now())

# Combine date and time into single datetime object
selected_datetime = datetime.datetime.combine(start_date, start_time)

col3, col4 = st.columns(2)

with col1:
    pickup_lon = st.number_input(label='Enter pickup longitute', format="%.6f", value=-73.950655)

with col2:
    pickup_lat = st.number_input(label='Enter pickup latitute', format="%.6f", value=40.783282)

col5, col6 = st.columns(2)

with col5:
    dropoff_lon = st.number_input(label='Enter dropoff longitute', format="%.6f", value=-73.984365)

with col6:
    dropoff_lat = st.number_input(label='Enter dropoff latitute', format="%.6f", value=40.769802)

# passenger_count = st.number_input(label='Enter passenger count', min_value=1, max_value=4, value=1)

passenger_count = st.selectbox(label='Select passenger count', options=[1, 2, 3, 4], index=0)

ride_params = {
    "pickup_datetime": selected_datetime.isoformat(),
    "pickup_longitude": pickup_lon,
    "pickup_latitude": pickup_lat,
    "dropoff_longitude": dropoff_lon,
    "dropoff_latitude": dropoff_lat,
    "passenger_count": int(passenger_count)
}

# st.write(params)

API_URL = 'https://taxifare-126048618009.europe-west1.run.app/predict'


# Display the parameters
# st.write("Your fare estimation summary:")


st.subheader("_Your fare estimation summary_", divider=True)

st.write("Selected Date and Time:", selected_datetime)
st.write("Pickup location:", pickup_lon, ",", pickup_lat)
st.write("Dropoff location:", dropoff_lon, ",", dropoff_lat)
st.write("Number of passengers:", passenger_count)


# Start play with ChatGPT

# Create a route layer to visualize the route from pickup to dropoff
route_data = [
    [pickup_lon, pickup_lat],  # Pickup point
    [dropoff_lon, dropoff_lat]  # Dropoff point
]

# Create the map with route
view_state = pdk.ViewState(
    latitude=(pickup_lat + dropoff_lat) / 2,
    longitude=(pickup_lon + dropoff_lon) / 2,
    zoom=12,
    pitch=0,
)

# Create the route line (bold and clear)
route_layer = pdk.Layer(
    "PathLayer",
    data=[{"path": route_data}],  # Path data in the correct format
    get_path="path",
    get_width=8,  # Increased width
    get_color=[255, 0, 0],  # Red color for better visibility
)

# Solid Circle for Start (with dotted effect)
start_marker = pdk.Layer(
    "ScatterplotLayer",
    data=[{"coordinate": [pickup_lon, pickup_lat]}],
    get_position="coordinate",
    get_radius=120,  # Radius of the circle
    get_fill_color=[0, 255, 0, 255],  # Green color for the start point
    get_line_color=[0, 255, 0],  # Green color for the outline
    get_line_width=4,  # Dotted effect (via line width)
    pickable=True,
)

# Solid Circle for End
end_marker = pdk.Layer(
    "ScatterplotLayer",
    data=[{"coordinate": [dropoff_lon, dropoff_lat]}],
    get_position="coordinate",
    get_radius=120,  # Radius of the circle
    get_fill_color=[255, 0, 0, 255],  # Red color for the solid circle
    get_line_color=[255, 0, 0],  # Red color for the outline
    get_line_width=3,  # Solid line for the end point
    pickable=True,
)

# Add letters "S" and "E" as text labels
text_layer = pdk.Layer(
    "TextLayer",
    data=[
        {"position": [pickup_lon, pickup_lat], "text": "S", "size": 24, "color": [0, 0, 0]},
        {"position": [dropoff_lon, dropoff_lat], "text": "E", "size": 24, "color": [0, 0, 0]},
    ],
    get_position="position",
    get_text="text",
    get_size="size",
    get_color="color",
    pickable=True
)

# Create the deck with the route layer and markers
deck = pdk.Deck(
    layers=[route_layer, start_marker, end_marker, text_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/streets-v11"
)

# Display the map immediately when the user inputs the data
st.pydeck_chart(deck)

# End play with ChatGPT


if st.button(label='Click to predict'):
    response = requests.get(API_URL, params=ride_params)

    result = response.json()
    predicted_result = result.get("fare", "N/A")

    st.success(f'🚖 Predicted fare: ${predicted_result: .2f}')
    st.write(predicted_result)


        # response = requests.get(API_URL, params=ride_parameters)
        # response.raise_for_status()  # Raise error if API request fails

        # # Parse JSON response
        # result = response.json()
        # predicted_fare = result.get("fare", "N/A")  # Get fare amount from API response


# For comparison

'''
---
'''
# st.title("Taxi Fare Prediction")

# # Date and Time Input
# selected_date = st.date_input("Select a Date", value=datetime.date.today())
# selected_time = st.time_input("Select a Time", value=datetime.datetime.now().time())

# # Combine Date and Time
# selected_datetime = datetime.datetime.combine(selected_date, selected_time)

# # Pickup Location Inputs
# pickup_longitude = st.number_input("Enter Pickup Longitude", format="%.6f", value=-73.950655)
# pickup_latitude = st.number_input("Enter Pickup Latitude", format="%.6f", value=40.783282)

# # Dropoff Location Inputs
# dropoff_longitude = st.number_input("Enter Dropoff Longitude", format="%.6f", value=-73.984365)
# dropoff_latitude = st.number_input("Enter Dropoff Latitude", format="%.6f", value=40.769802)

# # Passenger Count Input
# passenger_count = st.number_input("Enter Passenger Count", min_value=1, max_value=10, step=1, value=1)

# # API URL (Replace with your actual API endpoint)
# # API_URL = "https://taxifare.lewagon.ai/predict"

# # Build the API Parameters Dictionary
# ride_parameters = {
#     "pickup_datetime": selected_datetime.isoformat(),
#     "pickup_longitude": pickup_longitude,
#     "pickup_latitude": pickup_latitude,
#     "dropoff_longitude": dropoff_longitude,
#     "dropoff_latitude": dropoff_latitude,
#     "passenger_count": int(passenger_count),
# }

# # Submit button
# if st.button("Predict Fare"):
#     try:
#         # Call the API
#         response = requests.get(API_URL, params=ride_parameters)
#         response.raise_for_status()  # Raise error if API request fails

#         # Parse JSON response
#         result = response.json()
#         predicted_fare = result.get("fare", "N/A")  # Get fare amount from API response

#         # Display prediction
#         st.write(result)
#         st.success(f"🚖 Estimated Fare: **${predicted_fare:.2f}**")

#     except requests.exceptions.RequestException as e:
#         st.error(f"API request failed: {e}")

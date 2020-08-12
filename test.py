import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import pydeck as pdk
df3=pd.read_csv("https://raw.githubusercontent.com/napoles-uach/covid19mx/master/estadoslatlon.csv")
#map_data = pd.DataFrame(
#    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#    columns=['lat', 'lon'])

df=pd.DataFrame()
df[['lat','lon']]=df3[['Lat','Long']]


#df = pd.DataFrame(
#    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#    columns=['lat', 'lon'])


st.subheader('Streamlit para visualizar mapas desde github v2')
#map_data = df
#st.map(map_data)

#####################
DATA_URL = "https://raw.githubusercontent.com/ajduberstein/sf_public_data/master/bay_area_commute_routes.csv"
# A bounding box for downtown San Francisco, to help filter this commuter data
DOWNTOWN_BOUNDING_BOX = [
    -122.43135291617365,
    37.766492914983864,
    -122.38706428091974,
    37.80583561830737,
]


def in_bounding_box(point):
    """Determine whether a point is in our downtown bounding box"""
    lng, lat = point
    in_lng_bounds = DOWNTOWN_BOUNDING_BOX[0] <= lng <= DOWNTOWN_BOUNDING_BOX[2]
    in_lat_bounds = DOWNTOWN_BOUNDING_BOX[1] <= lat <= DOWNTOWN_BOUNDING_BOX[3]
    return in_lng_bounds and in_lat_bounds


df = pd.read_csv(DATA_URL)
# Filter to bounding box
df = df[df[["lng_w", "lat_w"]].apply(lambda row: in_bounding_box(row), axis=1)]

GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]


#######################


st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=37.75,#19.4,
         longitude=-122.43,#-99.13,
         zoom=11,
         pitch=10,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=3000,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
            "ArcLayer",
            data=df,
            get_width="S000 * 2",
            get_source_position=["lng_h", "lat_h"],
            get_target_position=["lng_w", "lat_w"],
            get_tilt=15,
            get_source_color=RED_RGB,
            get_target_color=GREEN_RGB,
            pickable=True,
            auto_highlight=True,
            ),
    
#         pdk.Layer(
#             'ScatterplotLayer',
#             data=df,
#             get_position='[lon, lat]',
#             get_color='[200, 30, 0, 160]',
#             get_radius=3000,
#         ),
     ],
 ))

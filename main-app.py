import streamlit as st
import pandas as pd
import pydeck as pdk

from urllib.error import URLError

@st.cache
def from_data_file(filename):
    url = (
        "https://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/%s" % filename)
    return pd.read_json(url)



if __name__ == '__main__':

    df = pd.read_excel('CitiesBySunshineDurationWithCoordinates.xlsx')

    try:
        st.sidebar.markdown('### Map Layers')
        selected_month = st.sidebar.select_slider('Month', options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ALL_LAYERS = {
            "My Layer": pdk.Layer(
                "ScatterplotLayer",
                data=df,
                pickable=True,
                opacity=0.8,
                stroked=True,
                filled=True,
                radius_scale=500,
                # radius_scale=60,
                radius_min_pixels=2,
                radius_max_pixels=60,
                line_width_min_pixels=1,
                get_position=['Longitude', 'Latitude'],
                get_radius=selected_month,
                get_fill_color=[255, 255, 0],
                get_line_color=[0, 0, 0],
            )
        }
        selected_layers = [
            layer for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)]
        if selected_layers:
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={"latitude": 0,
                                    "longitude": -122.4, "zoom": 0, "pitch": 0},
                layers=selected_layers,
                tooltip={"text": "{City}, {Country}\n" + selected_month + ': {' + selected_month + '}'}
            ))
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error("""
            **This demo requires internet access.**

            Connection error: %s
        """ % e.reason)
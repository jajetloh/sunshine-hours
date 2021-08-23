import streamlit as st
import pandas as pd
import pydeck as pdk

from urllib.error import URLError

def hex_to_rgb(h):
    '''Takes a hex rgb string (e.g. #ffffff) and returns an RGB tuple (float, float, float).'''
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

class LinearColourInterpolator:
    interpolate = None
    def __init__(self, rgb_min, rgb_max, n_min, n_max):
        def value_to_rgb(value):
            rgb1 = rgb_min
            rgb2 = rgb_max
            if value <= n_min:
                return rgb1
            elif value >= n_max:
                return rgb2
            return [i1 + (i2 - i1) * (value - n_min)/(n_max - n_min) for i1, i2 in zip(rgb1, rgb2)]
        self.interpolate = value_to_rgb

if __name__ == '__main__':

    df = pd.read_excel('CitiesBySunshineDurationWithCoordinates.xlsx')
    df_melt = pd.melt(df, id_vars=['Continent', 'Country', 'City', 'Latitude', 'Longitude'], value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], var_name='Month', value_name='Sunshine')

    # Min and max values found in all individual months
    n_min = min(df_melt['Sunshine'].values)
    n_max = max(df_melt['Sunshine'].values)

    try:
        st.sidebar.markdown('### Month Selection')
        selected_month = st.sidebar.select_slider('Month', options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        
        st.sidebar.markdown('### Colours')

        selected_min_colour = st.sidebar.color_picker('Min Colour')
        selected_max_colour = st.sidebar.color_picker('Max Colour')

        lci = LinearColourInterpolator(hex_to_rgb(selected_min_colour), hex_to_rgb(selected_max_colour), n_min, n_max)
        df_melt['Colour'] = [lci.interpolate(v) for v in df_melt['Sunshine'].values]

        ALL_LAYERS = {
            "Sunshine Hours": pdk.Layer(
                "ColumnLayer",
                data=df_melt[df_melt['Month'] == selected_month],
                get_position=['Longitude', 'Latitude'],
                get_elevation='Sunshine',
                elevation_scale=2e4,
                radius=1e5,
                pickable=True,
                auto_highlight=True,
                opacity=0.7,
                get_fill_color='Colour',
            ),
        }

        st.sidebar.markdown('### Map Layers')
        selected_layers = [
            layer for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)]

        if selected_layers:
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={"latitude": 0,
                                    "longitude": -122.4, "zoom": 0.1, "pitch": 10},
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
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

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

    df = pd.read_excel('CitiesBySunshineDurationWithDaylight.xlsx')

    try:
        st.sidebar.markdown('### Month Selection')
        selected_month = st.sidebar.select_slider('Month', options=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        
        # Note: should match with ALL_LAYERS keys
        DEPENDENT_VAR_MAP = {'Sunshine Hours': 'Sunshine', 'Daylight Hours': 'Daylight', 'Sunshine Ratio': 'Sunshine Ratio'}

        st.sidebar.markdown('### Column Height')
        selected_layer = st.sidebar.selectbox('Height Value', list(DEPENDENT_VAR_MAP.keys()))

        st.sidebar.markdown('### Colours')
        selected_colour_property = st.sidebar.selectbox('Colour Value', list(DEPENDENT_VAR_MAP.keys()))

        selected_min_colour = st.sidebar.color_picker('Min Colour', '#FFFFCA')
        selected_max_colour = st.sidebar.color_picker('Max Colour', '#EF9200')

        # Min and max values found in all individual months
        n_min = min(df[DEPENDENT_VAR_MAP[selected_colour_property]].values)
        n_max = max(df[DEPENDENT_VAR_MAP[selected_colour_property]].values)

        lci = LinearColourInterpolator(hex_to_rgb(selected_min_colour), hex_to_rgb(selected_max_colour), n_min, n_max)
        df['Colour'] = [lci.interpolate(v) for v in df[DEPENDENT_VAR_MAP[selected_colour_property]].values]

        df['Latitude truncated'] = np.round(df['Latitude'], 4)
        df['Longitude truncated'] = np.round(df['Longitude'], 4)
        df['Daylight truncated'] = np.round(df['Daylight'], 2)
        # Using 'Sunshine Ratio' in get_elevation seems to be buggy, so renamed to fix
        df['Sunshine_Ratio'] = df['Sunshine Ratio']
        df['Ratio percent'] = [str(n) + '%' for n in np.round(100*df['Sunshine Ratio'], 1)]

        ALL_LAYERS = {
            "Sunshine Hours": pdk.Layer(
                "ColumnLayer",
                data=df[df['Month'] == selected_month],
                get_position=['Longitude', 'Latitude'],
                get_elevation='Sunshine',
                elevation_scale=9e6/max(df['Sunshine'].values),
                radius=1e5,
                pickable=True,
                auto_highlight=True,
                opacity=0.7,
                get_fill_color='Colour',
            ),
            "Daylight Hours": pdk.Layer(
                "ColumnLayer",
                data=df[df['Month'] == selected_month],
                get_position=['Longitude', 'Latitude'],
                get_elevation='Daylight',
                elevation_scale=9e6/max(df['Daylight'].values),
                radius=1e5,
                pickable=True,
                auto_highlight=True,
                opacity=0.7,
                get_fill_color='Colour',
            ),
            "Sunshine Ratio": pdk.Layer(
            "ColumnLayer",
                data=df[df['Month'] == selected_month],
                get_position=['Longitude', 'Latitude'],
                get_elevation='Sunshine_Ratio',
                elevation_scale=9e6/max(df['Sunshine_Ratio'].values),
                radius=1e5,
                pickable=True,
                auto_highlight=True,
                opacity=0.7,
                get_fill_color='Colour',
            ),
        }

        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v9",
            initial_view_state={"latitude": 0,
                                "longitude": 12, "zoom": 0.35, "pitch": 10},
            layers=ALL_LAYERS[selected_layer],
            tooltip={
                'html': '<b>{City}, {Country}</b> ({Longitude truncated}, {Latitude truncated})<br/>'
                    + f'{selected_month}</br>'
                    + 'Sunshine hours per month: {Sunshine}<br/>'
                    + 'Daylight hours per day: {Daylight truncated}<br/>'
                    + 'Sunshine ratio (Sunshine/Daylight): {Ratio percent}'
            }
        ))
    except URLError as e:
        st.error("""
            **This demo requires internet access.**

            Connection error: %s
        """ % e.reason)
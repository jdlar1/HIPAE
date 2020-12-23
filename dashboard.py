import glob

import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go

path = './data/D131120.csv'
dataset_path_list = glob.glob('.\\data\\*.csv')
# token = "pk.eyJ1IjoiamRsYXIiLCJhIjoiY2tqMHNjam41MXdybTJycndzN21hdWZ5MSJ9.2K__BBnNu5G-3kvmMdMcQA"
# px.set_mapbox_access_token(token)
variables = ['imuAx', 'imuAy', 'imuAz', 'imuCx',
             'imuCy', 'imuCz', 'imuGx', 'imuGy', 'imuGz',
             'T_1', 'P', 'A_2', 'Time_Data', 'T_3', 'RH', 'T_2',
             'NH3', 'CO', 'NO', 'C3H8', 'C4H10', 'CH4', 'H2', 'C2H5OH'
             ]

# --------------------------SIDEBAR--------------------------
st.sidebar.subheader('Opciones')
dataset_path_selected = st.sidebar.multiselect('Datasets', dataset_path_list)
variable = st.sidebar.selectbox('variable', variables)
grid_points = st.sidebar.checkbox('Puntos en grid')
# --------------------------SIDEBAR--------------------------


@st.cache
def load_dataset(filename):
    return pd.read_csv(filename)


if len(dataset_path_selected) > 0:
    loaded_data = load_dataset(dataset_path_selected[0])
    for dataset in dataset_path_selected[1:]:
        loaded_data = loaded_data.append(
            load_dataset(dataset), ignore_index=True)


# -----------------------------MAIN------------------------------
st.title('Visualización de mapas')


# ----------------------------PUNTOS-----------------------------
st.subheader('Puntos')
@st.cache
def get_points_fig(dataframe, variable):
    fig = px.scatter_mapbox(dataframe, lat="lat", lon="lot", color=f"{variable}", color_continuous_scale="Viridis")
    fig.update_layout(mapbox_style="open-street-map")
    return fig

if len(dataset_path_selected) > 0:
    points_fig = get_points_fig(loaded_data, variable)
    st.plotly_chart(points_fig)

# ---------------------------CONTORNO----------------------------
# st.subheader('Contorno')


# @st.cache
# def get_contour_fig(dataframe, variable):
#     fig = go.Figure(go.Densitymapbox(lat=dataframe.lat,
#                                      lon=dataframe.lot, 
#                                      z=dataframe[f"{variable}"], 
#                                      radius=15))
#     fig.update_layout(mapbox_style="open-street-map", mapbox_center_lon=-74)
#     fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#     return fig


# if len(dataset_path_selected) > 0:
#     contour_fig = get_contour_fig(loaded_data, variable)
#     st.plotly_chart(contour_fig)


# ----------------------------GRID-----------------------------
st.subheader('Grid')

grid_size = st.slider('Tamaño del grid', 8, 18, 12)

@st.cache
def get_grid_fig(dataframe, variable):
    fig = ff.create_hexbin_mapbox(
        data_frame=loaded_data, lat="lat", lon="lot",
        nx_hexagon=grid_size, agg_func=np.mean, opacity=0.4, labels={"color": f"{variable}"},
        min_count=False, color=f"{variable}", color_continuous_scale="Viridis", show_original_data=grid_points
    )
    fig.update_layout(mapbox_style="open-street-map")
    return fig


if len(dataset_path_selected) > 0:
    grid_fig = get_grid_fig(loaded_data, variable)
    st.plotly_chart(grid_fig)

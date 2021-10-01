import pandas as pd
import numpy as np
import sqlite3 as sql
import time

import streamlit as st

path_climate = 'https://climatecharts.net/'
path_terminal = 'https://www.searates.com/maritime/'

path_charact = 'https://raw.githubusercontent.com/vcubo/beta_06/main/VCUBO_PRCHARv01.csv'
path_projects = 'https://raw.githubusercontent.com/vcubo/beta_06/main/VCUBO_PRTABLEv01.csv'

df_char = pd.read_csv(path_charact)
df_proj = pd.read_csv(path_projects)

char_dict = {''}

#st.write(df_char)
#st.write(df_proj)

# DATABASE CONNECTION
conn = sql.connect('beta_projects.db')
#df_proj.to_sql('beta_projects', conn)

df_projects = pd.read_sql('SELECT * FROM beta_projects', conn)
#st.write(len(df_projects))
data01 = st.expander("SQL DB", expanded=True)
with data01:
    st.write(df_projects)


st.session_state.clients_list = ['-']+df_char[~df_char['CLIENT_SIZE'].isna()]['CLIENT_SIZE'].unique().tolist()
st.session_state.protype_list = ['-']+df_char[~df_char['PROJ_TYPE'].isna()]['PROJ_TYPE'].unique().tolist()
st.session_state.prosize_list = ['-']+df_char[~df_char['PROJ_SIZE'].isna()]['PROJ_SIZE'].unique().tolist()
st.session_state.prphase_list = ['-']+df_char[~df_char['PHASE'].isna()]['PHASE'].unique().tolist()
st.session_state.country_list = ['-']+df_char[~df_char['COUNTRY1'].isna()]['COUNTRY1'].unique().tolist()
st.session_state.climate_list = ['-']+df_char[~df_char['CLIMATE'].isna()]['CLIMATE'].unique().tolist()
st.session_state.elevate_list = ['-']+df_char[~df_char['ELEVATION'].isna()]['ELEVATION'].unique().tolist()
st.session_state.citysiz_list = ['-']+df_char[~df_char['CITY_SIZE'].isna()]['CITY_SIZE'].unique().tolist()
st.session_state.citydis_list = ['-']+df_char[~df_char['CITY_DIST'].isna()]['CITY_DIST'].unique().tolist()
st.session_state.termdis_list = ['-']+df_char[~df_char['TERM_DIST'].isna()]['TERM_DIST'].unique().tolist()
st.session_state.contype_list = ['-']+df_char[~df_char['CONTR_TYPE'].isna()]['CONTR_TYPE'].unique().tolist()
st.session_state.contras_list = ['-']+df_char[~df_char['CONTR_SIZE'].isna()]['CONTR_SIZE'].unique().tolist()
st.session_state.greenfl_list = ['-']+df_char[~df_char['GREENFIELD'].isna()]['GREENFIELD'].unique().tolist()
st.session_state.prefabr_list = ['-']+df_char[~df_char['PREFAB'].isna()]['PREFAB'].unique().tolist()

pr_reg01 = st.expander("L1 SETUP", expanded=True)
with pr_reg01:
    a01,a02, a03, = st.columns(3)
#L1 FACTORS
    with a01: sel_clients = st.selectbox('CLIENT SIZE', st.session_state.clients_list)
    with a02: sel_protype = st.selectbox('PROJECT TYPE', st.session_state.protype_list)
    with a03: sel_prosize = st.selectbox('PROJECT SIZE', st.session_state.prosize_list)
    #create_pr = st.button('CREATE PROJECT')

#L2 FACTORS
pr_reg02 = st.expander("L2 SETUP", expanded=True)
with pr_reg02:
    b01,b02, b03, b04 = st.columns(4)
    with b01:
        sel_prphase = st.selectbox('PROJECT PHASE', st.session_state.prphase_list)
        sel_country = st.selectbox('COUNTRY', st.session_state.country_list)
    with b02:
        sel_climate = st.selectbox('CLIMATE', st.session_state.climate_list, help=path_climate)
        sel_elevate = st.selectbox('SITE ELVATION', st.session_state.elevate_list)
    with b03:
        sel_citysiz = st.selectbox('NEAREST CITY SIZE',st.session_state.citysiz_list)
        sel_citydis = st.selectbox('NEAREST CITY DISTANCE', st.session_state.citydis_list)
    with b04:
        sel_termdis = st.selectbox('NEAREST TERMINAL DISTANCE',st.session_state.termdis_list, help=path_terminal)
    #add_l2 = st.button("ADD LEVEL2  ")

# L3 FACTORS
pr_reg03 = st.expander("L3 SETUP", expanded=True)
with pr_reg03:
    c01,c02, c03, c04 = st.columns(4)
    with c01: sel_contype = st.selectbox('CONTRACT TYPE', st.session_state.contype_list)
    with c02: sel_contras = st.selectbox('MAIN CONTRACTOR', st.session_state.contras_list)
    with c03: sel_greenfl = st.selectbox('GREENFIELD %', st.session_state.greenfl_list)
    with c04: sel_prefabr = st.selectbox('PREFABRICATE %', st.session_state.prefabr_list)

#pr_reg04 = st.expander("L3 DATES", expanded=True)
#with pr_reg04:
    d01, d02, d03, d04 = st.columns(4)
    with d01: sel_bl_start = st.date_input('BL START')
    with d02: sel_bl_finis = st.date_input('BL FINISH')
    with d03: sel_ac_start = st.date_input('ACTUAL START')
    with d04: sel_ac_finis = st.date_input('ACTUAL FINISH')
add_reg = st.button('ADD REGISTER')


def form_callback():
    st.write(st.session_state.my_slider)
    st.write(st.session_state.my_checkbox)

#with st.form(key='my_form'):
#    slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
#    checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
#    submit_button = st.form_submit_button(label='Submit', on_click=form_callback)

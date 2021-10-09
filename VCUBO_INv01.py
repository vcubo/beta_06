import pandas as pd
import numpy as np
import sqlite3 as sql
import psycopg2
import time

import streamlit as st

path_climate = 'https://climatecharts.net/'
path_terminal = 'https://www.searates.com/maritime/'

path_charact = 'https://raw.githubusercontent.com/vcubo/beta_06/main/VCUBO_PRCHARv01.csv'
path_projects = 'https://raw.githubusercontent.com/vcubo/beta_06/main/VCUBO_PRTABLEv01.csv'
path_csvtemp = '/Users/facu/Desktop/VCUBO/02 PRODUCT/beta_06/test_pr/'
path_csvtemp2 = 'https://raw.githubusercontent.com/vcubo/beta_06/main/test_pr/'
path_csvend = 'v01.csv'

df_char = pd.read_csv(path_charact)
df_proj = pd.read_csv(path_projects)

char_dict = {''}

@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return psycopg2.connect(**st.secrets["postgres_prod"])

conn2 = init_connection()

@st.cache(ttl=600)
def run_query(query):
    with conn2.cursor() as cur:
        cur.execute(query)
        conn2.commit()


# DATABASE CONNECTION
conn = sql.connect('beta_projects.db')
#df_proj.to_sql('beta_projects', conn)
df_projects = pd.read_sql('SELECT * FROM beta_projects', conn)

if 'pr_df' not in st.session_state:
    st.session_state.pr_df = df_projects.copy()
if 'rg_df1' not in st.session_state:
    st.session_state.rg_df1 = df_projects.copy()
    st.session_state.rg_df2 = df_projects.copy()

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

st.header('PORJECTS UPLOAD')
st.caption('VCUBO beta v0.6')
st.subheader('1. COMPLETAR DATOS')
with st.form('reg_upload'):
    a1, a2 = st.columns(2)
    with a1: st.session_state.COM_ID = st.text_input('COMPANY ID')
    with a2: st.session_state.L1_ID = st.text_input('PROJECT ID')
    st.markdown('***')
    #st.markdown('LEVEL 1')
    a01,a02, a03, = st.columns(3)
#L1 FACTORS
    with a01: sel_clients = st.selectbox('CLIENT SIZE', st.session_state.clients_list)
    with a02: sel_protype = st.selectbox('PROJECT TYPE', st.session_state.protype_list)
    with a03: sel_prosize = st.selectbox('PROJECT SIZE', st.session_state.prosize_list)
    #create_pr = st.button('CREATE PROJECT')
    st.markdown('***')
#L2 FACTORS
    #st.markdown('LEVEL 2')
    b01,b02, b03, b04 = st.columns(4)
    with b01:
        sel_prphase = st.selectbox('PROJECT PHASE', st.session_state.prphase_list)
        sel_country = st.selectbox('COUNTRY', st.session_state.country_list)
    with b02:
        sel_climate = st.selectbox('CLIMATE', st.session_state.climate_list, help=path_climate)
        sel_elevate = st.selectbox('SITE ELEVATION', st.session_state.elevate_list)
    with b03:
        sel_citysiz = st.selectbox('NEAREST CITY SIZE',st.session_state.citysiz_list)
        sel_citydis = st.selectbox('NEAREST CITY DISTANCE', st.session_state.citydis_list)
    with b04:
        sel_termdis = st.selectbox('NEAREST TERMINAL DISTANCE',st.session_state.termdis_list, help=path_terminal)
    #add_l2 = st.button("ADD LEVEL2  ")
    st.markdown('***')
# L3 FACTORS
    #st.markdown('LEVEL 3')
    c01,c02, c03, c04 = st.columns(4)
    with c01: sel_contype = st.selectbox('CONTRACT TYPE', st.session_state.contype_list)
    with c02: sel_contras = st.selectbox('MAIN CONTRACTOR', st.session_state.contras_list)
    with c03: sel_greenfl = st.selectbox('GREENFIELD %', st.session_state.greenfl_list)
    with c04: sel_prefabr = st.selectbox('PREFABRICATE %', st.session_state.prefabr_list)
    st.markdown('***')
# DATES
    st.markdown('DATES')
    d01, d02, d03, d04 = st.columns(4)
    with d01: sel_bl_start = st.date_input('BL START')
    with d02: sel_bl_finis = st.date_input('BL FINISH')
    with d03: sel_ac_start = st.date_input('ACTUAL START')
    with d04: sel_ac_finis = st.date_input('ACTUAL FINISH')
    add_reg = st.form_submit_button('CHECK REGISTER')
    if add_reg:
        st.session_state.rg_df1['COM_ID'][0] = st.session_state.COM_ID
        st.session_state.rg_df1['L1_ID'][0] = st.session_state.L1_ID
        st.session_state.rg_df1['COUNTRY1'][0] = sel_country
        st.session_state.rg_df1['PROJ_TYPE'][0] = sel_protype
        st.session_state.rg_df1['PHASE'][0] = sel_prphase
        st.session_state.rg_df1['PROJ_SIZE'][0] = sel_prosize
        st.session_state.rg_df1['CONTR_TYPE'][0] = sel_contype
        st.session_state.rg_df1['GREENFIELD'][0] = sel_greenfl
        st.session_state.rg_df1['PREFAB'][0] = sel_prefabr
        st.session_state.rg_df1['CLIMATE'][0] = sel_climate
        st.session_state.rg_df1['ELEVATION'][0] = sel_elevate
        st.session_state.rg_df1['CITY_SIZE'][0] = sel_citysiz
        st.session_state.rg_df1['CITY_DIST'][0] = sel_citydis
        st.session_state.rg_df1['TERM_DIST'][0] = sel_termdis
        st.session_state.rg_df1['CLIENT_SIZE'][0] = sel_clients
        st.session_state.rg_df1['CONTR_SIZE'][0] = sel_contras
        st.session_state.rg_df1['BL_START'][0] = sel_bl_start
        st.session_state.rg_df1['BL_FINISH'][0] = sel_bl_finis
        st.session_state.rg_df1['AC_START'][0] = sel_ac_start
        st.session_state.rg_df1['AC_FINISH'][0] = sel_ac_finis
st.markdown('***')
st.subheader('2. PRECARGA DE REGISTROS')
show_table = st.checkbox('SHOW COMPLETE TABLE')
if show_table:
    st.table(st.session_state.rg_df1)
else:
    st.write(st.session_state.rg_df1)
add_reg = st.button('ADD REGISTER')
#st.write(st.session_state.rg_df1)
if add_reg:
    if st.session_state.pr_df['COM_ID'][0] == 'a':
        st.session_state.pr_df = st.session_state.rg_df1.copy()
    else:
        st.session_state.pr_df = st.session_state.pr_df.append(st.session_state.rg_df1, ignore_index=True)
st.markdown('***')
st.subheader("3. REGISTROS DE PROYECTO A SUBIR EN BASE DE DATOS")


#del_range = [i for i in range(len(st.session_state.pr_df))]
#st.write("DELETE ENTERED REGISTER")
#c01, c02 = st.columns((1,2))
#with c01:
#    del_index = st.selectbox('NUMBER', del_range)
#    del_reg = st.button('DELETE SELECTED REGISTER')
#if del_reg:
#    st.session_state.pr_df = st.session_state.pr_df.drop(int(del_index)).copy()


with st.form('upload_project'):
    if show_table: st.table(st.session_state.pr_df)
    else: st.write(st.session_state.pr_df)
    create = st.form_submit_button("Upload project")
    if create:
        for i in range(len(st.session_state.pr_df)):
            upload_query = f"INSERT INTO pr_main (com_id, l1_id, l2_id, country1, country2, proj_type, phase, proj_size, contr_type, greenfield, prefab, climate, elevation, city_size, city_dist, term_dist, client_size, contr_size, bl_start, bl_finish, ac_start, ac_finish) VALUES('{st.session_state.pr_df['COM_ID'][i]}','{st.session_state.pr_df['L1_ID'][i]}','{st.session_state.pr_df['L2_ID'][i]}','{st.session_state.pr_df['COUNTRY1'][i]}','{st.session_state.pr_df['COUNTRY2'][i]}','{st.session_state.pr_df['PROJ_TYPE'][i]}','{st.session_state.pr_df['PHASE'][i]}','{st.session_state.pr_df['PROJ_SIZE'][i]}','{st.session_state.pr_df['CONTR_TYPE'][i]}','{st.session_state.pr_df['GREENFIELD'][i]}','{st.session_state.pr_df['PREFAB'][i]}','{st.session_state.pr_df['CLIMATE'][i]}','{st.session_state.pr_df['ELEVATION'][i]}','{st.session_state.pr_df['CITY_SIZE'][i]}','{st.session_state.pr_df['CITY_DIST'][i]}','{st.session_state.pr_df['TERM_DIST'][i]}','{st.session_state.pr_df['CLIENT_SIZE'][i]}','{st.session_state.pr_df['CONTR_SIZE'][i]}','{st.session_state.pr_df['BL_START'][i]}','{st.session_state.pr_df['BL_FINISH'][i]}','{st.session_state.pr_df['AC_START'][i]}','{st.session_state.pr_df['AC_FINISH'][i]}');"
            st.caption(f'uploading (running query): {upload_query}')

            run_query(upload_query)
        st.success("Project uploaded (waiting for review)")
st.markdown('***')

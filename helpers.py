import sqlite3
import shutil
import datetime
import pandas as pd
import streamlit as st


def get_data(db, tbl):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query(f'select * from {tbl}', conn)
    conn.close()
    return df

def Generate_new_DRS(shipName, db, tbl):

    numberOfRows = len(df_currDRS)

#     wb = xw.book('_DRS V55.xlsm')  # load as openpyxl workbook; useful to keep the original layout
#     # which is discarded in the following dataframe
#     # df = pd.read_excel('_DRS V55.xlsm')  # load as dataframe (modifications will be easier with pandas API!)
#     ws = wb.sheets['DRSEND']
#     for i in numberOfRows:
#         ws.range('A8').insert()
#
#
#
# df_all_data[['delay_hr', 'downtime_hr', 'VET_risk']] = df_all_data[['delay_hr', 'downtime_hr', 'VET_risk']]\
#     .apply(pd.to_numeric, errors='coerce', axis=1) # make the three cols numeric
# drsHeaders = df_all_data.columns.values
# # st.dataframe(drsHeaders)
# df_to_display = df_all_data[df_all_data['ship_name'].isin(['Taiga','Takasago']) ]
# df_to_display = df_to_display[df_to_display['dt_ocurred'].str.contains('2022') | df_to_display['done_dt'].str.contains('2022') ]
# # df_to_display = df_to_display[df_to_display['status'].str.contains('2')]
# st.write(df_to_display)

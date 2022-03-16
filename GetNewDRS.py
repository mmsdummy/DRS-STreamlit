import pandas as pd
import streamlit as st
from helpers import get_data
import xlwings as xw
from datetime import date
import os
print('---GetNewDRS----')
st.set_page_config(page_title='Generate new DR sender', layout='wide')
disp_cols = ['dt_ocurred','target_dt','done_dt', 'ser_no','nc_detail','est_cause_ship', 'init_action_ship','init_action_ship_dt',
             'final_action_ship','final_action_ship_dt', 'co_eval',
             'reason_rc','corr_action','rpt_by','insp_by','insp_detail','update_by', 'update_dt',
             'ext_dt','ext_rsn', 'req_num','ext_cmnt', 'sys_code', 'eq_code','ship_name']
# st.markdown('<style>.ReactVirtualized__Grid__innerScrollContainer div[class^="row"], .ReactVirtualized__Grid__innerScrollContainer div[class^="data row"]{ background:lightyellow; } </style>', unsafe_allow_html=True)

def writeToXL(ship, df_curr):
    ''' Module write toXL
    Input ship name and filtered df with observations for current year
    Extracts the data for DR sender for the current year and makes a new DR sender
     '''
    numberOfRows = len(df_curr)
    filename = r'_DRS V55.xlsm' #
    book = xw.Book(filename, password='mms@user')# Get template file
    ws = book.sheets['DRSEND']
    # appli = xw.App()
    app = xw.apps.active
    for i in range(numberOfRows):
            ws.range('A8').insert()# shift named ranges in excel to prevent overwriting
    ws.range('C1').value = ship
    f_name = str(date.today().year) + '_' + ship + '_DRS_V55.xlsm'
    new_drs_file = os.path.join('temp', f_name)
    ws.range('A8').options(index=False, header=False).value = df_curr # write dataframe to excel
    # checstatus()
    book.save(new_drs_file)# save excel as new file
    app.quit()
    return new_drs_file

def downloadXL():
    curr_year = date.today().year
    st.markdown(f'Generate new **{curr_year} DR sender**')
    df_rawData = get_data('master.sqlite', 'drsend') # get raw data to work upon
    vsl_list = sorted(list(df_rawData['ship_name'].unique()))
    # st.write(vsl_list)
    # vsl_list = [x.upper() for x in vsl_list]
    col1, col2, col3 = st.columns(3)
    with col2:
        shipName = st.selectbox('Select Vessel', vsl_list) # CHoose vessel from list of shipnames
    df_rawData[['delay_hr', 'downtime_hr', 'VET_risk']] = df_rawData[['delay_hr', 'downtime_hr', 'VET_risk']] \
        .apply(pd.to_numeric, errors='coerce', axis=1) # Convert to prevent errors

    #df_currDRS = df_rawData[(df_rawData['ship_name'] == shipName) & (df_rawData['dt_ocurred'].str.contains(curr_year))] # | (df_rawData['done_dt'].str.contains(curr_year)) | (df_rawData['status'].str.contains('OPEN')))]# Get current year data in new dataframe
    df_currDRS = df_rawData.query(f"ship_name == '{shipName}' and  (dt_ocurred.str.contains('{curr_year}') or done_dt.str.contains('{curr_year}') or status.str.contains('OPEN'))", engine='python')
    # df_currDRS = df_rawData[(df_rawData['ship_name'] == shipName) & (df_rawData['alert_req'].str.contains('v55_2022'))]  # new logic for filterig current DR sender
    with col1:
        st.markdown(f'{shipName} DR Sender being prepared. Please wait....')
    new_file = writeToXL(shipName, df_currDRS)
    with col1:
        st.info(f'Done... {shipName} DR Sender has {len(df_currDRS)} entries for {curr_year}.')
    st.write(df_currDRS[disp_cols]) # display only selected columns
    with open(new_file, 'rb') as f:
        st.download_button(f'Download {shipName} DR Sender', f, file_name=new_file[4:])

if st.download_button:
    downloadXL()

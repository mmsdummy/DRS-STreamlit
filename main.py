import pandas as pd
import streamlit as st
import sqlite3, shutil
print('-------------')

df = []
drsHeaders = []


def main():
    st.set_page_config(page_title='DRS 2022 Multi Page', layout='wide')
    global drsHeaders, df
    if 'loadState' not in st.session_state:
        st.session_state.loadState = False

    if st.button('Load data') or st.session_state.loadState:
        st.session_state.loadState = True
        sql3db = 'drsend1.sqlite'  # destination db
        shutil.copyfile(r'C:\Shares\drsapp\drsend.sqlite', sql3db)
        conn = sqlite3.connect(sql3db)
        df = pd.read_sql_query('select * from dr_sender', conn)
        conn.close()
        #  Load dataframe
        conn = sqlite3.connect('drsend.sqlite')
        df = pd.read_sql_query('select * from dr_sender', conn)
        conn.close()
        df[['delay_hr', 'downtime_hr', 'VET_risk']] = df[['delay_hr', 'downtime_hr', 'VET_risk']] \
            .apply(pd.to_numeric, errors='coerce', axis=1)  # make the three cols numeric
        drsHeaders = df.columns.values
        dfSelected = df[['ship_name', 'dt_ocurred', 'ser_no', 'def_code', 'nc_detail']]
        print('Data loading complete-----------')
        # , 'init_action_ship','final_action_ship','reason_rc','status', 'Severity', 'delay_hr', 'downtime_hr', 'brkdn_tf', 'critical_eq_tf', 'blackout_tf', 'docking_tf', 'coc_tf']]
        # st.dataframe(dfSelected)

    pages = {      # Register pages
        "DRS 2022 Home": drs_home,
        "Dashboard": drs_dash,
        "Filter Data": drs_filter,
        "Up/Download DRS": drs_up_dn,
    }
    st.sidebar.title("DRS 2022 App")
    # page = st.sidebar.selectbox("Select page", tuple(pages.keys()))
    page = st.sidebar.radio("Select page", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page]()
    print(len(drsHeaders))

def drs_home():
    global df, drsHeaders
    st.title("DRS 2022 Home")
    print('in home')
    #  Load dataframe

def drs_dash():
    print('in dashboard')
    st.title("DRS 2022 Dasboard")

def drs_filter():
    st.title("DRS Data Filter")
    print('in filter')

def drs_up_dn():
    global drsHeaders, df
    # drsHeaders = st.session_state.drsHeaders
    st.title("DRS Data Upload / Download")
    print('in upload / download')
    upldSection = st.expander('Upload vessel DR Sender (under Construction)')
    ucol1, ucol2, ucol3 = upldSection.columns(3)
    with upldSection:
        uploaded_file = st.file_uploader('Choose a file')
        if uploaded_file is not None:
            dfVslDrs = pd.read_excel(uploaded_file, sheet_name='DRSEND', skiprows=6, dtype=str,
                                     na_filter=False, parse_dates=False, usecols='A:CV')
            # import data from excel with all col=str and do not put <NA> for missing data
            filename = uploaded_file.name
            dfVslDrs.drop(dfVslDrs.index[-1], inplace=True)  # drop the last row - with ZZZ
            vsldfShape = dfVslDrs.shape
            st.write('Raw data from Vessel:', (vsldfShape[0]), 'Records found in "',
                     filename, '" (', vsldfShape[1], 'Columns)')
            dfVslDrs.columns = drsHeaders  # rename the headers for Vessel file, same as master db
            # convert long datetime to date
            toCorrect = ['dt_ocurred', 'init_action_ship_dt', 'target_dt', 'final_action_ship_dt', 'done_dt',
                         'update_dt']
            for someCol in toCorrect:
                dfVslDrs[someCol] = pd.to_datetime(dfVslDrs[someCol]).apply(lambda x: x.date())

            drsID = list(dfVslDrs["DRS_ID"])  # get list of DRS_ID for checking new data
            dfNoCommon = df[~df['DRS_ID'].isin(drsID)]  # filter OUT all rows with common DRS_ID
            st.write(len(df[df['DRS_ID'].isin(drsID)]), "common items found and updated with latest info.", )
            dfUpdated = pd.concat([dfNoCommon, dfVslDrs], ignore_index=True)  # add all the new rows to dataframe
            st.dataframe(dfVslDrs)  # diplay DF
            conn = sqlite3.connect('new.sqlite')  # write complete data to new database for check
            dfUpdated.to_sql('dr_sender', conn, if_exists='replace', index=False)
            conn.close()


if __name__ == '__main__':
    main()

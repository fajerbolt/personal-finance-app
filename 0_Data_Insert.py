import pandas as pd

import streamlit as st


st.header('Insert and Edit your Expenses Data')

insert_method = st.radio('**Select data insert method**', ['File Upload and Edit', 'Manual Insert'], horizontal=True)

if insert_method == 'Manual Insert':
    #Manual Data Insert through date editor and empty dataframe
    st.subheader('Insert your Expense Details')
    st.markdown('Make sure your data is as you want it. Once you leave this page, for any further edit you will have to restart the insert process.')
    empty_df = pd.DataFrame(columns=['Year', 'Month', 'Category', 'Subcategory', 'Amount']).reset_index()
    df = st.data_editor(empty_df, num_rows='dynamic')
    st.session_state.df = df
else:
    #Data Uploader
    uploaded_data = st.file_uploader('Upload a CSV or an Excel File')
    #Upload data
    if uploaded_data is not None:
        try:
            df = pd.read_csv(uploaded_data, thousands=',')
        except:
            df = pd.read_excel(uploaded_data, thousands=',')
        else:
            'Uploaded file is not CSV or Excel file'
    #Display and provide editing of data
    if uploaded_data is not None:
        st.subheader('Review and Edit your Data')
        st.markdown('Make sure your data is as you want it. Once you leave this page, for any further edit you will have to restart the upload and edit process.')
        df = st.data_editor(df, num_rows='dynamic')
        st.session_state.df = df
    
    else:
        st.empty()

import pandas as pd
import math

import streamlit as st
import altair as alt

from datetime import date
from dateutil.relativedelta import relativedelta
import calendar


#Import Data
if 'df' not in st.session_state:
    st.header('Insert your data on Data Insert page')
elif 'df' in st.session_state and st.session_state.df.Amount.sum() == 0:
    st.header('Insert non-zero amounts in your data')
else:
    df = st.session_state.df
    data = df.copy()

    #Data Formatting
    data.Amount = data.Amount.astype(int)

    data['Month'] = data['Month'] + ' ' + data['Year'].astype(str)


    #########DASHBOARD############
    #Filters
    st.sidebar.header('Filter Data')

    with st.sidebar:
        selected_periods = st.multiselect('Months to count expenses for', data.Month.unique(), default=data.Month.unique())
        
    data = data[data['Month'].isin(selected_periods)]
    
    #Dashboard
    st.header('When are you reaching your savings goal')

    col1, col2, col3 = st.columns(3)
    #Current Savings
    with col1:
        savings = st.number_input('What are your current savings', min_value=0)
    #Insert Goal Amount
    with col2:
        goal = st.number_input('What is your savings goal', min_value=0)
    #Insert Monthly Income
    with col3:
        income = st.number_input('What is your monthly income', min_value=0)
    #Calculate
    mean_expense = round(data.Amount.sum()/data.Month.nunique(), 1)
    monthly_savings = income - mean_expense
    months_to_goal = math.ceil((goal-savings)/monthly_savings)
    date_of_goal = date.today() + relativedelta(months=+months_to_goal)
    yearly_savings = format(int(monthly_savings*13), ',')

    if goal == 0 or income == 0:
        st.markdown('**Insert values for goal and income in fields above**')
    else:
        st.markdown(f'You will reach your savings goal by the end of **{calendar.month_name[date_of_goal.month]} {date_of_goal.year}**, if your monthly expenses and income stay the same.')
        st.markdown(f'**This time next year** (end of month) you will be richer by approximately **{yearly_savings}**')
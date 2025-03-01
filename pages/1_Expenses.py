import pandas as pd

import streamlit as st
import altair as alt


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

    data['Year'] = pd.to_datetime(data.Date).dt.year
    data['Month'] = pd.to_datetime(data.Date).dt.month_name()

    #########DASHBOARD############
    st.sidebar.header('Filter Data')

    st.header('Breakdown of Expenses by Month')

    with st.sidebar:
        selected_categories = st.multiselect('Categories', data.Category.unique(), default=data.Category.unique())
        selected_periods = st.multiselect('Months', data.Month.unique(), default=data.Month.unique())

    data = data[data['Category'].isin(selected_categories)]
    data = data[data['Month'].isin(selected_periods)]

    #Average and Median Monthly Expenditures
    mean_expense = format(round(data.Amount.sum()/data.Month.nunique(), 1), ',')
    incomes_by_month = data.groupby(['Year', 'Month']).sum()['Amount']
    median_expense = format(incomes_by_month.median(), ',')
    total_expense = format(data.Amount.sum(), ',')

    st.subheader('Average Expenses')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label='Average Monthly Expenses:', value=mean_expense)

    with col2:
        st.metric(label='Median Monthly Expenses:', value=median_expense)

    with col3:
        st.metric(label='Total Spent:', value=total_expense)


    #Expenses by Month
    st.subheader('Expenses by Month')

    incomes_by_month = incomes_by_month.reset_index()

    incomes_by_month['month_number'] = pd.to_datetime(incomes_by_month.Month, format='%B').dt.month
    incomes_by_month = incomes_by_month.sort_values(by=['Year', 'month_number'])

    bar_chart = alt.Chart(incomes_by_month).mark_bar().encode(
        x=alt.X('Month', sort=None),
        y='Amount',
    )
    st.altair_chart(bar_chart, use_container_width=True)


    #Expenses by Month by Category
    st.subheader('Expenses by Month per Category')

    incomes_by_month_cat = data.groupby(['Year', 'Month', 'Category']).sum()['Amount']
    incomes_by_month_cat = incomes_by_month_cat.reset_index()

    incomes_by_month_cat['month_number'] = pd.to_datetime(incomes_by_month.Month, format='%B').dt.month
    incomes_by_month_cat = incomes_by_month_cat.sort_values(by=['Year', 'month_number'])

    #Number of categories for width of the chart
    num_categories = incomes_by_month_cat['Category'].nunique()

    bar_chart2 = alt.Chart(incomes_by_month_cat).mark_bar().encode(
        x=alt.X('Month', sort=None, axis=None),
        y='Amount',
        color=alt.Color('Month', sort=incomes_by_month_cat.Month.unique()),
        column=alt.Column('Category', header=alt.Header(orient='bottom'))
    ).properties(
        width=525/num_categories
    )
    st.altair_chart(bar_chart2)


    #Expenses per subcategory
    st.subheader('Expenses per Subcategory')

    categories_list = ['']
    categories_list.extend(list(data.Category.unique()))
    category_to_analyze = st.selectbox(label='Select a category from the dropdown to draw a chart', options=categories_list, index=0)

    if category_to_analyze == '':
        st.empty()
    else:
        data = data[data['Category']==category_to_analyze]

        incomes_by_month_subcat = data.groupby(['Year', 'Month', 'Subcategory']).sum()['Amount']
        incomes_by_month_subcat = incomes_by_month_subcat.reset_index()

        incomes_by_month_subcat['month_number'] = pd.to_datetime(incomes_by_month_subcat.Month).dt.month
        incomes_by_month_subcat = incomes_by_month_subcat.sort_values(by=['Year', 'month_number'])

        #Number of categories for width of the chart
        num_subcategories = incomes_by_month_subcat['Subcategory'].nunique()

        bar_chart3 = alt.Chart(incomes_by_month_subcat).mark_bar().encode(
            x=alt.X('Month', sort=None, axis=None),
            y='Amount',
            color=alt.Color('Month', sort=incomes_by_month_subcat.Month.unique()),
            column=alt.Column('Subcategory', header=alt.Header(orient='bottom'))
        ).properties(
            width=525/num_subcategories
        )
        st.altair_chart(bar_chart3)

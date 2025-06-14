#@rohitbedse_ → Indian Startup Analysis - using pandas and streamlit
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df = pd.read_csv('start_up_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg', str(round(avg_funding)) + ' Cr')
    with col4:
        st.metric('Funded Startups', num_startups)

    st.header('Month-on-Month (MoM) Investment Trend')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])

    # Ensure 'year' and 'month' columns exist
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    # Create a real datetime column for x-axis
    temp_df['date'] = pd.to_datetime(temp_df[['year', 'month']].assign(day=1))

    # Plot
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.plot(temp_df['date'], temp_df['amount'], marker='o')

    ax3.set_xlabel("Date")
    ax3.set_ylabel("Funding Amount (Cr)" if selected_option == 'Total' else "Funding Count")
    ax3.set_title(f"Month-on-Month {'Funding Amount' if selected_option == 'Total' else 'Funding Count'}")
    ax3.grid(True)
    fig3.autofmt_xdate()

    st.pyplot(fig3)



def load_investor_details(investor):
    st.title(investor)
    #load the recent 5 investments of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)
    
    col1, col2 = st.columns(2)
    with col1:
        big_series = df[df['investors'].str.contains(investor, case=False, na=False)] \
                        .groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor, case=False, na=False)] \
                        .groupby('vertical')['amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Sectors Invested In')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series.values, labels=vertical_series.index, autopct="%0.1f%%")
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        round_series = df[df['investors'].str.contains(investor, case=False, na=False)] \
                    .groupby('round')['amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Rounds Invested In')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series.values, labels=round_series.index, autopct="%0.1f%%")
        st.pyplot(fig2)

    with col4:
        # (\) is used to continue long lines in short lines in python
        city_series = df[df['investors'].str.contains(investor, case=False, na=False)] \
                    .groupby('city')['amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Cities Invested In')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series.values, labels=city_series.index, autopct="%0.1f%%")
        st.pyplot(fig3)
        
    df['year'] = df['date'].dt.year

    # Safe, case-insensitive filtering
    year_series = df[df['investors'].str.contains(investor, case=False, na=False)] \
                .groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    ax4.plot(year_series.index, year_series.values, marker='o')
    ax4.set_xlabel("Year")
    ax4.set_ylabel("Total Investment (₹)")
    ax4.set_title(f"Year-over-Year Investment by {investor}")
    fig4.tight_layout()
    st.pyplot(fig4)


        
st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

else:
    st.title("Investor Details")
    selected_investor = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
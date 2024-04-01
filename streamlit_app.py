import streamlit as st
import pandas as pd
import math
from pathlib import Path
st.set_page_config(page_title='GDP Dashboard',)
def get_gdp_data():
    """Grab GDP data from a CSV file."""
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)
    MIN_YEAR = 1980
    MAX_YEAR = 2022
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    return gdp_df
gdp_df = get_gdp_data()
'''
# : GDP Dashboard
Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website.
'''
''
min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()
from_year, to_year = st.slider(
    'From which years do you want data ?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])
countries = gdp_df['Country Code'].unique()
if not len(countries):
    st.warning("Select at least one country")
selected_countries = st.multiselect('Which countries would you like to see data of?',countries,['IND', 'USA','JPN'])
''
''
# Filter the data
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
]
st.header('GDP v/s time graph')
''
st.line_chart(filtered_gdp_df,x='Year',y='GDP',color='Country Code',)
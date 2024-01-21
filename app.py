import streamlit as st
import pandas as pd
from Repository import PortfolioRepository
from st_aggrid import AgGrid
from st_pages import Page, Section, add_page_title, show_pages, show_pages_from_config

st.set_page_config(layout='wide')
show_pages_from_config(".streamlit/pages.toml")

# Streamlit commands to display the web app
st.title('Список криптопортфелей')


def get_portfolios():
    df = pd.DataFrame()
    for portfolio in PortfolioRepository.get_all_portfolios():
        row = pd.DataFrame([{
            'Name': portfolio.name,
            'Numeraire': portfolio.numeraire,
            'Purchase_period': portfolio.purchase_period}])

        df = pd.concat([df, row], ignore_index=True)
    return df


def show_aggrid(df):
    AgGrid(df)


show_aggrid(get_portfolios())

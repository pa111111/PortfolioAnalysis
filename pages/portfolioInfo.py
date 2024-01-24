import streamlit as st
import pandas as pd
from Repository import PortfolioRepository
from st_aggrid import AgGrid

from Service import PortfolioManager

st.title('About portfolios')


def get_portfolios():
    df = pd.DataFrame()
    for portfolio in PortfolioRepository.get_all_portfolios():
        row = pd.DataFrame([{
            'Name': portfolio.name,
            'Numeraire': portfolio.numeraire,
            'Purchase_period': portfolio.purchase_period}])

        df = pd.concat([df, row], ignore_index=True)
    return df


def get_portfolio_elements(portfolio_name):
    portfolio = PortfolioRepository.get_portfolio(portfolio_name)
    df = pd.DataFrame()

    for element in portfolio.get_portfolio_elements():
        row = pd.DataFrame([{
            'Symbol': element.asset.symbol,
            'Numeraire': portfolio.numeraire,
            'Purchase_period': portfolio.purchase_period,
            'Volume': element.volume,
            'Period_start': element.period_start,
            'Period_end': element.period_end}])
        df = pd.concat([df, row], ignore_index=True)
    return df


def get_portfolio_transactions(portfolio_name):
    return PortfolioManager.emulate_portfolio_element_transactions(portfolio_name)


def show_aggrid(df):
    AgGrid(df)


portfolio_name = st.selectbox('Select portfolio', get_portfolios()['Name'])

st.markdown('List of cryptocurrency in portfolio: '+portfolio_name)
show_aggrid(get_portfolio_elements(portfolio_name))
st.markdown('List of emulated transactions')
show_aggrid(PortfolioManager.emulate_portfolio_element_transactions(portfolio_name))

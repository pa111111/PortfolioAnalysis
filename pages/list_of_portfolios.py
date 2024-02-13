import dash
from dash import html, dash_table, dcc
from dash.dependencies import Input, Output
import pandas as pd
from Service import PortfolioManager
from app import app


# Функция для создания URL
def create_analysis_link(portfolio_name):
    return f"[show_analysis](/portfolio-analysis?portfolio_name={portfolio_name})"


# получаем список портфелей
portfolios_df = PortfolioManager.get_all_portfolios()
# добавляем столбец со ссылкой на portfolio_analysis.py
portfolios_df['Analysis Link'] = portfolios_df['name'].apply(lambda x: create_analysis_link(x))

# Макет приложения
layout = html.Div([
    dcc.Store(id='memory_store'),
    # Заголовок для первой таблицы
    html.H2("List of portfolios"),
    # Таблица для списка портфолио
    dash_table.DataTable(
        id='tbl_portfolios',
        columns=[{"name": i, "id": i} for i in portfolios_df.columns if i != 'Analysis Link'] + [
            {"name": 'Analysis', "id": 'Analysis Link', 'type': 'text', 'presentation': 'markdown'}],
        data=portfolios_df.to_dict('records'),
        sort_action='native',  # Включает сортировку по столбцам
        filter_action='native',
        style_table={'margin-bottom': '20px'},  # Отступ между таблицами
        style_header={'backgroundColor': '#305D91', 'padding': '10px', 'color': '#FFFFFF', 'font-weight': 'bold',
                      'text-align': 'center'},
        style_data={'text-align': 'left'},
        style_cell={'min-width': '1px'},
        fill_width=False,
        row_selectable='single',  # Разрешить выбор строки
        markdown_options={"link_target": "_blank"}
    ),
    # Заголовок для второй таблицы
    html.H2("List of portfolio assets"),
    dash_table.DataTable(
        id='tbl_portfolio_elements',
        columns=[
            {'id': 'symbol', 'name': 'Актив'},
            {'id': 'period_start', 'name': 'Начало закупки'},
            {'id': 'period_end', 'name': 'Окончание закупки'},
            {'id': 'volume', 'name': 'Объем закупки'}
        ],
        sort_action='native',  # Включает сортировку по столбцам
        style_header={'backgroundColor': '#305D91', 'padding': '10px', 'color': '#FFFFFF', 'font-weight': 'bold',
                      'text-align': 'center'},
        style_data={'text-align': 'left'},
        style_cell={'min-width': '1px'},
        fill_width=False
    ),
    html.H2("Cumulative portfolio trades"),
    dash_table.DataTable(
        id='tbl_cumulative_portfolio_trades',
        columns=[{'id': col, 'name': col} for col in ['Symbol', 'Date', 'Price', 'Coins_bought', 'Investment_amount',
                                                      'Cumulative_investment_by_asset',
                                                      'Cumulative_coins_bought_by_asset', 'Current_value_by_asset',
                                                      'Profit_loss_by_asset', 'Profit_loss_percent_by_asset']],
        sort_action='native',  # Включает сортировку по столбцам
        style_header={'backgroundColor': '#305D91', 'padding': '10px', 'color': '#FFFFFF', 'font-weight': 'bold',
                      'text-align': 'center'},
        style_data={'text-align': 'left'},
        style_cell={'min-width': '1px'},
        fill_width=False
    ),
    html.H2("Portfolio summary"),
    dash_table.DataTable(
        id='tbl_portfolio_summary',
        columns=[{'id': col, 'name': col} for col in
                 ['Date', 'Total_Current_Value', 'Total_Investment', 'Total_Profit_Loss',
                  'Total_Profit_Loss_Percent']],
        sort_action='native',  # Включает сортировку по столбцам
        style_header={'backgroundColor': '#305D91', 'padding': '10px', 'color': '#FFFFFF', 'font-weight': 'bold',
                      'text-align': 'center'},
        style_data={'text-align': 'left'},
        style_cell={'min-width': '1px'},
        fill_width=False
    )
])


# Сохраняем в store portfolio_name
@app.callback(Output('memory_store', 'data'),
              [Input('tbl_portfolios', 'derived_virtual_data'),
               Input('tbl_portfolios', 'selected_rows')])
def select_portfolio(all_rows_data, selected_rows):
    if selected_rows and all_rows_data:
        selected_row_index = selected_rows[0]
        selected_row_data = all_rows_data[selected_row_index]
        portfolio_name = selected_row_data['name']
        return portfolio_name
    return ''


@app.callback(Output('tbl_portfolio_elements', 'data'),
              Input('memory_store', 'data'))
def fill_portfolio_elements(data):
    if data != '':
        elements_data = PortfolioManager.get_portfolio_elements(data)
        return elements_data.to_dict('records')
    return None


@app.callback(Output('tbl_cumulative_portfolio_trades', 'data'),
              Input('memory_store', 'data'))
def fill_cumulative_portfolio_trades(data):
    if data != '':
        return PortfolioManager.get_cumulative_portfolio_info(data).to_dict('records')
    return None


@app.callback(Output('tbl_portfolio_summary', 'data'),
              Input('memory_store', 'data'))
def fill_portfolio_summary(data):
    if data != '':
        return PortfolioManager.get_portfolio_summary(data).to_dict('records')
    return None

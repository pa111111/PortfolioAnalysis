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

portfolio_elements_df = pd.DataFrame(columns=['symbol', 'period_start', 'period_end', 'volume'])

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

    # Таблица для списка активов портфолио
    dash_table.DataTable(
        id='tbl_portfolio_elements',
        columns=[{"name": i, "id": i} for i in portfolio_elements_df.columns],
        data=portfolio_elements_df.to_dict('records'),
        sort_action='native',  # Включает сортировку по столбцам
        style_header={'backgroundColor': '#305D91', 'padding': '10px', 'color': '#FFFFFF', 'font-weight': 'bold',
                      'text-align': 'center'},
        style_data={'text-align': 'left'},
        style_cell={'min-width': '1px'},
        fill_width=False
    ),
    html.H2("Cumulative portfolio trades"),

    html.H2("Portfolio summary"),
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
    elements_data = PortfolioManager.get_portfolio_elements(data)
    return elements_data.to_dict('records')


# @app.callback(
#     Output('table-portfolio-elements', 'data'),
#     [Input('table-portfolios', 'derived_virtual_data'),
#      Input('table-portfolios', 'selected_rows')]
# )
# def update_elements(all_rows_data, selected_rows):
#     if selected_rows and all_rows_data:
#         selected_row_index = selected_rows[0]
#         selected_row_data = all_rows_data[selected_row_index]
#         portfolio_name = selected_row_data['name']
#
#         # Теперь получаем данные элементов портфеля, используя выбранное имя портфеля
#         elements_data = PortfolioManager.get_portfolio_elements(portfolio_name)
#         return elements_data.to_dict('records')
#     return []

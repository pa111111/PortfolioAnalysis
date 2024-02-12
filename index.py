from dash import html, dcc
from dash.dependencies import Input, Output
import pages.list_of_portfolios, pages.portfolio_analysis, pages.edit_portfolio, pages.list_of_assets
from app import app

# Словарь для маппинга URL на макеты страниц
PAGE_ROUTES = {
    '/list-of-portfolios': pages.list_of_portfolios.layout,
    '/portfolio-analysis': pages.portfolio_analysis.layout,
    '/edit-portfolio': pages.edit_portfolio.layout,
    '/list-of-assets': pages.list_of_assets.layout
}

pages.portfolio_analysis.register_callbacks(app)  # Измененный вызов функции


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # Боковое меню
    html.Div([
        html.H2("Menu", style={'textAlign': 'center'}),
        dcc.Link('List of portfolios', href='/list-of-portfolios', style={'display': 'block', 'margin': '10px'}),
        dcc.Link('Portfolio analysis', href='/portfolio-analysis', style={'display': 'block', 'margin': '10px'}),
        dcc.Link('Edit portfolio', href='/edit-portfolio', style={'display': 'block', 'margin': '10px'}),
        dcc.Link('List of assets', href='/list-of-assets', style={'display': 'block', 'margin': '10px'}),
        # Добавьте дополнительные ссылки на страницы
    ], style={'width': '20%', 'float': 'left', 'height': '100vh', 'borderRight': '2px solid black', 'padding': '20px'}),

    # Основное содержимое
    html.Div(id='page-content', style={'width': '70%', 'float': 'left', 'padding': '20px'})
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(f"URL pathname: {pathname}")  # Отладочное сообщение
    return PAGE_ROUTES.get(pathname, pages.list_of_portfolios.layout)

if __name__ == '__main__':
    app.run_server(debug=True)
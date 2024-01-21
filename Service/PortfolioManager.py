import pandas as pd

from Repository import PortfolioRepository, AssetRepository


def emulate_portfolio_element_transactions(portfolio_name):
    transactions_list = []
    portfolio = PortfolioRepository.get_portfolio(portfolio_name)
    for element in portfolio.get_portfolio_elements():
        investment_amount = element.volume
        frequency = _get_frequency(portfolio.purchase_period)
        df_prices = AssetRepository.get_asset_daily_prices(element.asset, portfolio.numeraire)
        for date in pd.date_range(element.period_start, element.period_end, freq=frequency):
            price = df_prices[df_prices['ts'] == date]['price'].values[0]
            transactions_list.append([element.asset.symbol, date, price,
                                      investment_amount / price, investment_amount])
    return pd.DataFrame(transactions_list,
                        columns=['Symbol', 'Date', 'Price', 'Coins_bought', 'investment_amount'])


def _get_frequency(purchase_period):
    frequency = ''
    if purchase_period == 'EveryMonth':
        frequency = 'M'
    elif purchase_period == 'EveryMonth':
        frequency = 'W'
    else:
        ValueError('Unknown purchase period')
    return frequency

import pandas as pd
from Repository import PortfolioRepository, AssetRepository
from Utils import Cache_utils


def get_all_portfolios():
    portfolios = PortfolioRepository.get_all_portfolios()
    # Преобразование списка объектов Portfolio в список словарей
    portfolios_dicts = [portfolio.to_dict() for portfolio in portfolios]
    return pd.DataFrame(portfolios_dicts)


def get_portfolio_elements(portfolio_name):
    portfolio_elements = PortfolioRepository.get_portfolio(portfolio_name).get_portfolio_elements()
    elements_dicts = [element.to_dict() for element in portfolio_elements]
    return pd.DataFrame(elements_dicts)


def emulate_portfolio_element_transactions(portfolio_name):
    transactions_list = []
    portfolio = PortfolioRepository.get_portfolio(portfolio_name)
    for element in portfolio.get_portfolio_elements():
        investment_amount = element.volume
        frequency = _get_frequency(portfolio.purchase_period)
        df_prices = AssetRepository.get_asset_daily_prices(element.asset, portfolio.numeraire, element.period_start,
                                                           element.period_end)
        for date in pd.date_range(element.period_start, element.period_end, freq=frequency):
            price = df_prices[df_prices['ts'] == date]['price'].values[0]
            transactions_list.append([element.asset.symbol, date, pd.to_numeric(price),
                                      pd.to_numeric(investment_amount / price), pd.to_numeric(investment_amount)])
    return pd.DataFrame(transactions_list,
                        columns=['Symbol', 'Date', 'Price', 'Coins_bought', 'Investment_amount'])


@Cache_utils.cache_it
def cumulative_portfolio_info(portfolio_name):
    transactions_df = emulate_portfolio_element_transactions(portfolio_name).copy()
    # Убедимся, что 'Date' в правильном формате и отсортировано
    transactions_df.sort_values(['Symbol', 'Date'], inplace=True)
    # Рассчитываем накопительный инвестиционный вклад для каждого актива
    transactions_df['Cumulative_investment_by_asset'] = transactions_df.groupby('Symbol')['Investment_amount'].cumsum()
    # Рассчитываем накопительный инвестиционный вклад для каждого актива
    transactions_df['Cumulative_coins_bought_by_asset'] = transactions_df.groupby('Symbol')['Coins_bought'].cumsum()
    # Рассчитываем накопленную стоимость инвестиционного актива для каждого актива
    transactions_df['Current_value_by_asset'] = transactions_df['Cumulative_coins_bought_by_asset'] * transactions_df['Price']
    # Рассчитываем прибыль/убытки инвестиционного актива для каждого актива
    transactions_df['Profit_loss_by_asset'] = transactions_df['Current_value_by_asset'] - transactions_df['Cumulative_investment_by_asset']
    # Расчет прибыли/убытка в процентах для каждого актива
    transactions_df['Profit_loss_percent_by_asset'] = (transactions_df['Profit_loss_by_asset'] / transactions_df['Cumulative_investment_by_asset']) * 100

    return transactions_df


def portfolio_summary(portfolio_name):
    cumulative_portfolio_df = cumulative_portfolio_info(portfolio_name).copy()
    # Суммирование по портфелю
    total_current_value = cumulative_portfolio_df.groupby('Date')['Current_value_by_asset'].sum()
    total_investment = cumulative_portfolio_df.groupby('Date')['Cumulative_investment_by_asset'].sum()
    total_profit_loss = cumulative_portfolio_df.groupby('Date')['Profit_loss_by_asset'].sum()

    # Расчет общего процента прибыли/убытка
    total_profit_loss_percent = (total_profit_loss / total_investment) * 100

    # Создание нового DataFrame для анализа портфеля
    portfolio_summary = pd.DataFrame({
                                'Total_Current_Value': total_current_value,
                                'Total_Investment': total_investment,
                                'Total_Profit_Loss': total_profit_loss,
                                'Total_Profit_Loss_Percent': total_profit_loss_percent
                            }).reset_index()

    return portfolio_summary


def _get_frequency(purchase_period):
    frequency = ''
    if purchase_period == 'EveryMonth':
        frequency = 'M'
    elif purchase_period == 'EveryMonth':
        frequency = 'W'
    else:
        ValueError('Unknown purchase period')
    return frequency


# Profitability Analysis (Анализ Прибыльности)
def profit_loss_calculation():
    return None

# Portfolio Distribution (Распределение Портфеля)
def portfolio_distribution_analysis():
    return None

# Price Change Analysis (Анализ Изменения Цены)
def price_change_analysis():
    return None

# Investment Volume Over Time (Объем Инвестиций По Времени)
def investment_volume_analysis():
    return None

# Total Profit/Loss Calculation (Расчет Общей Прибыли/Убытка)
def total_profit_loss_calculation():
    return None

# Volatility Analysis (Анализ Волатильности)
def volatility_analysis():
    return None

# Performance Comparison with the Market (Сравнение Производительности с Рынком)
def market_comparison_analysis():
    return None

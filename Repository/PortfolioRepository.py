from Repository import AssetRepository
from Repository.SessionContext import SessionContext
from Repository.db_uniswap import Portfolio as Portfolio_DB, AssetInPortfolio as AssetInPortfolio_DB
from Domain.Portfolio import Portfolio, PortfolioElement
from Domain.Assets import Asset


def get_portfolio(portfolio_name):
    with SessionContext() as session:
        portfolio_db = session.query(Portfolio_DB).filter_by(name=portfolio_name).first()
        portfolio = Portfolio(name=portfolio_db.name, numeraire=portfolio_db.numeraire,
                              purchase_period=portfolio_db.purchase_period.name)

        for element in _get_portfolio_element(portfolio.name):
            portfolio.add_portfolio_element(element)

    return portfolio


def _get_portfolio_element(portfolio_name):
    with SessionContext() as session:
        elements_db = session.query(Portfolio_DB, AssetInPortfolio_DB) \
            .join(Portfolio_DB, Portfolio_DB.id == AssetInPortfolio_DB.portfolio_id).filter_by(
            name=portfolio_name).all()
        portfolio_elements = []
        for element in elements_db:
            asset = AssetRepository.get_asset(element.AssetInPortfolio.asset.symbol)
            portfolio_element = PortfolioElement(asset=asset,
                                                 period_start=element.AssetInPortfolio.period_start,
                                                 period_end=element.AssetInPortfolio.period_end,
                                                 volume=element.AssetInPortfolio.volume)
            portfolio_elements.append(portfolio_element)
    return portfolio_elements


def _get_portfolio_element_transactions(portfolio: Portfolio):
    return None

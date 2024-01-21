from Repository import AssetRepository
from Service import PortfolioManager

#asset = AssetRepository.get_asset('ARB')
#prices = AssetRepository.get_asset_daily_prices(asset, 'WETH')

#print(prices)


PortfolioManager.emulate_portfolio_element_transactions('largeCap')

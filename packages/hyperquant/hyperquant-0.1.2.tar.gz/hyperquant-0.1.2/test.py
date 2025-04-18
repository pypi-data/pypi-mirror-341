import asyncio
from datetime import datetime, timedelta
from src.hyperquant.core import Exchange
from src.hyperquant.datavison.coinglass import CoinglassApi


async def main():
    api = CoinglassApi()
    await api.connect()
    df = await api.fetch_price_klines('Binance_BTCUSDT', datetime.now() - timedelta(days=1))
    print(df)
    await api.stop()

if __name__ == '__main__':
    asyncio.run(main())
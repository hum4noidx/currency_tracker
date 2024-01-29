# IT IS A DRAFT
import json

import websockets

symbols = ["BTC", "ETH", "USDTTRC", "USDTERC"]
currencies = ["RUB", "USDT"]

ws_url = "wss://stream.binance.com:9443/ws"


def get_stream_name(symbol, currency):
    return f"{symbol.lower()}{currency.lower()}@ticker"


async def handle_message(message):
    data = json.loads(message)
    # Extract the symbol, price, and quantity
    symbol = data["s"]
    price = float(data["c"])
    print(f"Saved {symbol} price: {price}")


async def fetch_and_save():
    # Create a list of stream names for all combinations of symbols and currencies
    streams = [
        get_stream_name(symbol, currency)
        for symbol in symbols
        for currency in currencies
    ]
    # Join the stream names with "/"
    streams = "/".join(streams)
    print(f"Streams: {streams}")
    # Connect to the websocket URL with the streams as a parameter
    async with websockets.connect(f"{ws_url}/{streams}") as ws:
        while True:
            message = await ws.recv()
            await handle_message(message)


# Run the connect function using asyncio
# asyncio.run(fetch_and_save())

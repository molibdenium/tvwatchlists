import requests
import pandas as pd

futures = requests.get(
    "https://fapi.binance.com/fapi/v1/exchangeInfo", verify=True, timeout=5)

ft = futures.json()["symbols"]

ftdf = []

for ticker in ft:
    ftdf.append("BINANCE:"+ticker["symbol"]+"PERP,")


ftdf = pd.DataFrame(ftdf)
fn = "binance_futures.txt"
x = ftdf.to_csv(fn, mode="w", header=False, index=False, sep=' ')


spot = requests.get(
    "https://api.binance.com/api/v3/exchangeInfo", verify=True, timeout=5)
spot = spot.json()["symbols"]

btclist = []
usdtlist = []

for ticker in spot:
    if ticker["quoteAsset"] == "BTC":
        if ticker["status"] != "BREAK":
            btclist.append("BINANCE:"+ticker["symbol"]+",")
    elif ticker["quoteAsset"] == "USDT":
        if ticker["symbol"][3:-4] not in ["BULL", "BEAR", "DOWN"]:
            if ticker["symbol"][-4] not in ["BULL", "BEAR", "DOWN"]:
                if ticker["symbol"][-2] not in ["UP"]:
                    if ticker["status"] != "BREAK":

                        usdtlist.append("BINANCE:"+ticker["symbol"]+",")

ftdf = pd.DataFrame(btclist)
x = ftdf.to_csv("binance_btc.txt", mode="w",
                header=False, index=False, sep=' ')

ftdf = pd.DataFrame(usdtlist)
x = ftdf.to_csv("binance_usdt.txt", mode="w",
                header=False, index=False, sep=' ')


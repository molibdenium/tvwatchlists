import requests
import pandas as pd
import csv

# FTX
ftx = requests.get("https://ftx.com/api/markets", verify=True, timeout=5)
ftx = ftx.json()["result"]

ftdf = [] # futures
spotdf = []
types = []
qc = []
token = []

def exclude_tickers(name):
    exclude = False
    elist = ["BEAR","BULL","HALF","HEDGE"]
    namelist = ["DAI","CAD","TRY","EUR","GBP","USD"]
    for e in elist:
        if e in name:
            exclude = True 
            break
    if name in namelist:
        exclude = True      

    return exclude


print("total symbols %s" % len(ftx))
for t in ftx:

    if t["type"] not in types:
        types.append(t["type"])
    if t["quoteCurrency"] not in qc:
        qc.append( t["quoteCurrency"])


    if t["type"] == "future":
        n = t["name"]
        n = str(n).replace("-","") 
        ftdf.append("FTX:"+n)
    elif t["type"] == "spot" and 'tokenizedEquity' not in t.keys():
        if t["quoteCurrency"] not in [None,"BTC","BRZ","EUR","TRYB","DOGE","USDT"]:
            if not exclude_tickers(t["baseCurrency"]):
                spotdf.append("FTX:"+t["baseCurrency"]+t["quoteCurrency"])
    elif t["type"] == "spot" and 'tokenizedEquity' in t.keys():
        token.append("FTX:"+t["baseCurrency"]+t["quoteCurrency"])



ftdf = pd.DataFrame(ftdf)
fn = "ftx_futures.txt"
x = ftdf.to_csv(fn, mode="w", header=False, index=False, sep=' ')

spotdf = pd.DataFrame(spotdf)
fn = "ftx_spot.txt"
x = spotdf.to_csv(fn, mode="w", header=False, index=False, sep=' ')

spotdf = pd.DataFrame(token)
fn = "ftx_tokenized.txt"
x = spotdf.to_csv(fn, mode="w", header=False, index=False, sep=' ')

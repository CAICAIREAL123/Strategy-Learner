
import pandas as pd
import numpy as np
import util
import matplotlib.pyplot as plt
import datetime as dt

def author():
    return 'ycai330'

def sma(data, symbol, lb = 14):
    output = data.rolling(window = lb).mean()
    output.dropna()
    output.fillna(method="ffill", inplace=True)
    output.fillna(method="bfill", inplace=True)
    #output = output[[symbol]]
    #df = pd.DataFrame(output)
    #df = df.dropna()
    #print(df['AAPL'])
    #print(df['AAPL'][0])
    return output
    
def bb(data, symbol, lb = 14):
    smA = data.rolling(window = lb, min_periods = lb).mean()
    smA = smA.dropna()
    rollingSTD = data.rolling(window = lb, min_periods = lb).std()
    rollingSTD = rollingSTD.dropna()
    top = 2 * rollingSTD + smA
    bot = -2 * rollingSTD + smA
    bb = (data - bot)/(top - bot)
    top_bb = top[symbol]
    bot_bb = bot[symbol]
    return top_bb, bot_bb

def Momentum(data, symbol,  lb = 14):
    
    return data/data.shift(lb - 1) - 1

def volat(data, lb = 10):
    output = data.rolling(window = lb).std()
    return output

def ema(data, lb):
    dt = pd.DataFrame.copy(data)
    dt.shift(lb-1)
    dt.iloc[lb-1] = data.iloc[0,0]
    k = lb + 1
    k = 2/k
    for i in range(len(dt)):
        if i > lb-1:
            dt.iloc[i] = data.iloc[i]*k + dt.iloc[i-1]*(1-k)
    dt[:lb-1] = np.nan
    dt.fillna(method = 'bfill', inplace = True)
    return dt

def main():
    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009,12,31)

    priceAll = util.get_data([symbol], pd.date_range(sd, ed), False)
    priceAll.fillna(method = 'bfill', inplace = True)
    priceAll.fillna(method = 'ffill', inplace = True)
    _df = priceAll[symbol]
    priceAllNorm = priceAll[symbol]/priceAll[symbol][0]
    df = pd.DataFrame(_df, index = priceAll.index)
    
    #  SMA
    smA, smANorm = sma(priceAll,symbol, 14)
    plt.title("Simple Moving Average")
    plt.xlabel("Dates")
    plt.ylabel("Normalized Value")
    plt.plot(smANorm, "b", label = "SMA")
    plt.plot(priceAllNorm, "r", label = "price")
    plt.plot(priceAllNorm/smANorm, "g", label = "price/SMA")
    plt.legend()
    plt.savefig("SMA.png")
    plt.clf()
    
    # Bollinger Bands
    top_bb, bot_bb = bb(priceAll, symbol, 14)
    plt.title("Bollinger Bands")
    plt.xlabel("Dates")
    plt.ylabel("Value")
    plt.plot(top_bb, "r", label = "Upper Band")
    plt.plot(bot_bb, "b", label = "Lower Band")

    plt.fill_between(top_bb.index.get_level_values(0), top_bb, bot_bb, color = '#ebecf0')
    plt.plot(priceAll[symbol], "g", label = "Price")
    plt.plot(smA, "y", label = "SMA")
    plt.legend()
    plt.savefig("BB.png")
    plt.clf()
    
    # Momentum
    price = Momentum(priceAll, symbol, 14)
    #print(price)
    plt.title("Momentum")
    plt.xlabel("Dates")
    plt.ylabel("Value")
    plt.plot(price, "r", label = "Momentum")
    plt.plot(priceAll[symbol], "b", label = "Price")
    #plt.hlines(y = [price.mean() - price.std(), price.mean() + price.std()], xmin = sd, xmax = ed, colors = 'black')
    #plt.hlines(y = [price.mean()], xmin = sd, xmax = ed, colors = 'black')
    plt.xlim(sd, ed)
    plt.legend()
    plt.savefig("Momentum.png")
    plt.clf()

if __name__ == "__main__":  
    main()
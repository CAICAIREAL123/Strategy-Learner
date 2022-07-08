import numpy as np
import pandas as pd
import datetime as dt
import util as ut
import matplotlib.pyplot as plt
import indicators as ind
import marketsimcode as mkt

class ManualStrategy(object):
    def __init__(self, verbose = False, impact = 0., commission = 0., short = -1, cash = 0, long = 1, shares = 1000, sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31)):
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.short = short
        self.cash = cash
        self.long = long
        self.shares = shares
        self.sd = sd
        self.ed = ed
        self.mkt = mkt
        self.ind = ind
    
    def author(self):
        return 'ycai330'
    
    

    
    def inSample(self, df, portValue, benchMark ):
        # initialize
        plt.figure(figsize = (14,7), dpi = 160)
        
        # benchmark
        plt.plot(benchMark, label = "Benchmark", color = "purple")
        # manual
        plt.plot(portValue, label = "Manual Strategy", color = "red")
        for i in range(1, len(df)):
            if df.iloc[i,0]>0:
                plt.axvline(x =  df.index[i], color = "blue")
            elif df.iloc[i,0]<0:
                plt.axvline(x = df.index[i], color = "black")
        # save
        plt.title("In sample: Manual Strategy & Benchmark")
        plt.legend(loc = "upper left")
        plt.xlim(self.sd, self.ed)
        plt.xlabel("Date")
        plt.ylabel("Normalized Return")
        plt.tick_params(axis = "x", labelrotation = 45)
        plt.savefig("in_sample_manual.png")
        plt.clf()
    
    def outSample(self, df, portValue, benchMark):
        # initialize
        plt.figure(figsize = (14, 7), dpi = 160)
        
        # benchmark
        plt.plot(benchMark, label = "Benchmark", color = "purple")
        # manual
        plt.plot(portValue, label = "Manual Strategy", color = "red")
        for i in range(len(df)):
            if df.iloc[i,0]>0:
                plt.axvline(x =  df.index[i], color = "blue")
            elif df.iloc[i,0]<0:
                plt.axvline(x = df.index[i], color = "black")
        # save
        plt.title("Out of sample: Manual Strategy & Benchmark")
        plt.legend(loc = "upper left")
        plt.xlim(self.sd, self.ed)
        plt.xlabel("Date")
        plt.ylabel("Normalized Return")
        plt.tick_params(axis = "x", labelrotation = 45)
        plt.savefig("out_of_sample_manual.png")
        plt.clf()
        
    
        
    def testPolicy(self, symbol = "JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000) :
        sym = [symbol]
        self.sd = sd
        self.ed = ed
        date = pd.date_range(sd, ed)
        price_all = ut.get_data(sym, date)
        price_all.dropna(inplace = True)
        price = price_all[sym]
        price_SPY = price_all["SPY"]
        
        sma = self.ind.sma(price, symbol, lb = 7)
        sma = price/sma
        
        bbT, bbB = self.ind.bb(price, sym, lb = 7)
        bbR = (price - bbB)/(bbT - bbB)
        
        mm = self.ind.Momentum(price, sym, lb = 7)
        
        lb = 7
        trade = pd.DataFrame(0, columns = ['Share'], index = price.index)
        share = 0
        #trade[symbol].values[:] = 0.
        for i in range(lb - 1, len(trade)-1):
            _s = sma.iloc[i, 0]
            _b = bbR.iloc[i, 0]
            _m = mm.iloc[i,0]
            #print(_s, _b, _m)
            flag_s1 = _s<1
            flag_s2 = _s>1
            flag_b1 = _b <= 0.6
            flag_b2 = _b >= 0.8
            flag_m1 = _m > 0.1
            flag_m2 = _m < 0
            if (flag_s1 and flag_b1) or (flag_s1 and flag_m1) or (flag_b1 and flag_m1):
               # price.iloc[i,0] = price.iloc[i,0]*(1+self.impact)
                if share ==-1000:
                    share = 1000
                    trade.iloc[i,0] = 2000
                elif share == 0:
                    share = 1000
                    trade.iloc[i,0] = 1000
            elif (flag_s2 and flag_b2) or (flag_s2 and flag_m2) or (flag_b2 and flag_m2):
                if share == 1000:
                    share = -1000
                    trade.iloc[i,0] = -2000
                elif share == 0:
                    share = -1000
                    trade.iloc[i,0] = -1000
                    
        if share > 0:
            trade.iloc[-1] = -1000.
        elif share < 0:
            trade.iloc[-1] = 1000.
        print(trade)
        #print(trade)
        return trade
def getDailyReturn(priceAll):
    return priceAll/priceAll.shift(1) - 1.

def circumulativeReturn(priceAll):
    return priceAll[-1]/priceAll[0]-1

def sharpRatio(dr, std):
    return np.sqrt(252.0)*((dr).mean()/std)
    
def getIndex(df):
    dr = getDailyReturn(df)
    return df, circumulativeReturn(df), dr.mean(), dr.std(), sharpRatio(dr, dr.std())

def benchMark(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000)  :
    date = pd.date_range(sd, ed)
    priceAllWithSPY = ut.get_data([symbol], date)
    priceAllWithSPY.dropna(inplace = True)
    priceAllWithSPY.fillna(method = 'bfill', inplace = True)
    priceAllWithSPY.fillna(method = 'ffill', inplace = True)
    df = pd.DataFrame(0, columns = ['Order'], index = priceAllWithSPY.index)
    df['Order'][0] = 1000
    output = []
    output.append((priceAllWithSPY.index[0], 1000))
    output.append((priceAllWithSPY.index[-1],  -1000))
    df = pd.DataFrame(output, columns = ['Date','Share'])
    return df.set_index('Date')

def main():
    manualStrategy = ManualStrategy(verbose  = False, impact = 0., commission = 0., short = -1, cash = 0, long = 1, shares = 1000, sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31))
    trade = manualStrategy.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000) 
    trade['Order'] = trade['Share'].apply(lambda x: 'BUY' if x>0 else 'SELL')
    trade.columns = trade.columns.str.replace('JPM', 'Share')
    trade['Symbol'] = "JPM"
    port = mkt.compute_portvals(trade, start_val = 100000)
    ptPortvals, ptCR, ptMean, ptSTD, ptSR = getIndex(port)
    df_bench = benchMark(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
    df_bench['Order'] = df_bench['Share'].apply(lambda x: 'BUY' if x>0 else 'SELL')
    df_bench['Symbol'] = "JPM"
    bchPortvals, bchCR, bchMean, bchSTD, bchSR = getIndex( mkt.compute_portvals(df_bench, 100000, 0.0, 0.0))
    print(f"Date Range: {dt.datetime(2008, 1, 1)} to {dt.datetime(2009,12,31)}")
    print()
    print(f"Sharp Ratio of Portfolio: {ptSR}")
    print(f"Sharp Ratio of benchmark : {bchSR}")
    print()
    print(f"Cumulative Return of Portfolio: {ptCR}")
    print(f"Cumulative Return of benchmark : {bchCR}")
    print()
    print(f"Stdev of Portfolio: {ptSTD}")
    print(f"Stdev of benchmark : {bchSTD}")
    print()
    print(f"Mean of daily returns of Portfolio: {ptMean}")
    print(f"Mean of daily returns of benchmark : {bchMean}")
    print()
    manualStrategy.inSample( trade, ptPortvals, bchPortvals )
    
    manualStrategy = ManualStrategy(verbose = False, impact = 0., commission = 0., short = -1, cash = 0, long = 1, shares = 1000, sd = dt.datetime(2010,1,1), ed = dt.datetime(2011,12,31))
    trade = manualStrategy.testPolicy(symbol = "JPM", sd = dt.datetime(2010,1,1), ed = dt.datetime(2011,12,31), sv = 100000) 
    trade['Order'] = trade['Share'].apply(lambda x: 'BUY' if x>0 else 'SELL')
    trade.columns = trade.columns.str.replace('JPM', 'Share')
    trade['Symbol'] = "JPM"
    port = mkt.compute_portvals(trade, start_val = 100000)
    ptPortvals, ptCR, ptMean, ptSTD, ptSR = getIndex(port)
    df_bench = benchMark(symbol="JPM", sd = dt.datetime(2010,1,1), ed = dt.datetime(2011,12,31), sv = 100000)
    df_bench['Order'] = df_bench['Share'].apply(lambda x: 'BUY' if x>0 else 'SELL')
    df_bench['Symbol'] = "JPM"
    bchPortvals, bchCR, bchMean, bchSTD, bchSR = getIndex( mkt.compute_portvals(df_bench, 100000, 0.0, 0.0))
    print(f"Date Range: {dt.datetime(2010, 1, 1)} to {dt.datetime(2011,12,31)}")
    print()
    print(f"Sharp Ratio of Portfolio: {ptSR}")
    print(f"Sharp Ratio of benchmark : {bchSR}")
    print()
    print(f"Cumulative Return of Portfolio: {ptCR}")
    print(f"Cumulative Return of benchmark : {bchCR}")
    print()
    print(f"Stdev of Portfolio: {ptSTD}")
    print(f"Stdev of benchmark : {bchSTD}")
    print()
    print(f"Mean of daily returns of Portfolio: {ptMean}")
    print(f"Mean of daily returns of benchmark : {bchMean}")
    print()
    manualStrategy.outSample( trade, ptPortvals, bchPortvals )
    
if __name__ == '__main__':
    main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
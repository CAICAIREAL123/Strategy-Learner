import numpy as np
import pandas as pd
import datetime as dt
import util as ut
import matplotlib.pyplot as plt
import ManualStrategy as manual
import StrategyLearner as stratg
import indicators as ind
import marketsimcode as mkt

class experiment1(object):
    def __init__(self):
        self.manual = manual.ManualStrategy(verbose = False, impact = 0.005, commission = 0.)
        self.stratg = stratg.StrategyLearner(verbose = False, impact = 0.005, commission = 0.)
        self.portm = None
        self.bchmk = None
        self.ports = None
        self.inSample = True
    
    def author(self):
        return 'ycai330'
    
    def getDailyReturn(self, data):
        #print(data)
        #print(np.shape(data))
        for i in range(1, len(data)):
            data.iloc[i] = data.iloc[i]/data.iloc[i-1]-1.
        data.iloc[0] = 0
        return data
    
    def trainSL(self, symbol, sd, ed, sv):
        self.stratg = stratg.StrategyLearner(verbose = False, impact = 0.005, commission = 0.)
        self.stratg.add_evidence(symbol = symbol, sd = sd, ed = ed, sv = sv)
    
    def exp(self, symbol, sd, ed, sv):
        sym = [symbol]
        date = pd.date_range(sd, ed)
        price_all = ut.get_data(sym, date)
        price_all.dropna(inplace = True)
        price = price_all[sym]
        price_SPY = price_all["SPY"]
        
        self.manual = manual.ManualStrategy(verbose = False, impact = 0.005, commission = 0., sd = sd, ed = ed)
        trade = self.manual.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = sv) 
        #trade.to_csv("ms1.csv")
        trade['Order'] = trade['Share'].apply(lambda x: 'BUY' if x>0 else 'SELL')
        trade.columns = trade.columns.str.replace(symbol, 'Share')
        trade['Symbol'] = symbol
        port = mkt.compute_portvals(trade, start_val = sv, commission = 0.00, impact = 0.005)
        #port.to_csv("ms2.csv")
        #port = port[20:]
        print(port.iloc[0])
        port = port/port.iloc[0]
        #port.to_csv("ms3.csv")
        #self.portm = port
        #print(port)
    
        df_bench = manual.benchMark(symbol = symbol, sd=sd, ed=ed, sv = sv) 
        df_bench['Order'] = df_bench['Share'].apply(lambda x: 'BUY' if x>0 else 'SELL')
        df_bench['Symbol'] = symbol
        
        bchmk = mkt.compute_portvals(df_bench, start_val = sv, commission = 0.00, impact = 0.005)
        
        #bchmk = bchmk[20:]
        bchmk = bchmk/bchmk.iloc[0]
        
        #self.bchmk = bchmk
        #print(bchmk)
        self.trainSL(symbol, sd, ed, sv)
        strat = self.stratg.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = sv) 
        strat.to_csv("ms1.csv")
        strat.columns = strat.columns.str.replace("Shares", 'Share')
        strat['Order'] = df_bench['Share'].apply(lambda x: 'BUY' if x>0 else 'SELL')
        strat['Symbol'] = symbol
        #print(strat)
        
        strat = mkt.compute_portvals(strat, start_val = sv, commission = 9.95, impact = 0.005)
        strat.to_csv("ms2.csv")
        #strat = strat[20:]
        strat = strat/strat.iloc[0]
        strat.to_csv("ms3.csv")
        #self.ports = strat
        #print(strat)
        return port, bchmk, strat
        
    def plotT(self, sd, ed, port, bchmk, strat):
        
        # initialize
        plt.figure(figsize = (12,6), dpi = 120)
        
        # benchmark
        plt.plot(bchmk, label = "Benchmark", color = "purple")
        # manual
        plt.plot(port, label = "Manual Strategy", color = "red")
        # strategy
        plt.plot(strat, label = "Strategy Learner", color = "blue")
        # save
       
        plt.legend(loc = "upper left")
        plt.xlim(sd, ed)
        plt.xlabel("Date")
        plt.ylabel("Normalized Return")
        plt.tick_params(axis = "x", labelrotation = 45)
        if self.inSample:
            plt.title("Experiment 1 in sample")
            plt.savefig("exp1_in.png")
        else:
            plt.title("Experiment 1 out of sample")
            plt.savefig("exp1_out.png")
        plt.clf()
        
        df = (port, bchmk, strat)
        dailyRet = []
        dailyAve = []
        stdEv = []
        crs = []
        for i in range(3):
            dailyRet.append(self.getDailyReturn(df[i]))
            dailyAve.append(np.mean(df[i]))
            stdEv.append(np.std(df[i]))
            crs.append(df[i].iloc[-1]/df[i].iloc[0] - 1.)
            
        table1 = pd.DataFrame(data = {"ms":[dailyRet[0], dailyAve[0], stdEv[0], crs[0]], 
                                      "bm":[dailyRet[1], dailyAve[1], stdEv[1], crs[1]], 
                                      "sl":[dailyRet[2], dailyAve[2], stdEv[2], crs[2]]},
                              index = {'dr','da', 'std', 'cr'})
        if self.inSample:
            table1.to_csv("exp1_tb1_in.csv")
        else:
            table1.to_csv("exp1_tb1_out.csv")
        table2 = pd.concat({"ms": port, "bm": bchmk, "sl": strat}, axis = 1)
        if self.inSample:
            table2.to_csv("exp1_tb2_in.csv")
        else:
            table2.to_csv("exp1_tb2_out.csv")
        
        
        
    
       

def main():
    exp1 = experiment1()
    exp1.inSample = True
    exp1.trainSL(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000) 
    port, bchmk, strat = exp1.exp( symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000) 
    exp1.plotT(dt.datetime(2008, 1, 1), dt.datetime(2009,12,31), port, bchmk, strat)
    exp1.inSample = False
    exp1.trainSL(symbol = "JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000) 
    port, bchmk, strat = exp1.exp( symbol = "JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000) 
    exp1.plotT(dt.datetime(2010, 1, 1), dt.datetime(2011,12,31), port, bchmk, strat)
            
        
        
if __name__ == '__main__':
    main()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
                            
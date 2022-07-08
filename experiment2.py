import numpy as np
import pandas as pd
import datetime as dt
import util as ut
import matplotlib.pyplot as plt
import ManualStrategy as manual
import StrategyLearner as stratg
import indicators as ind
import marketsimcode as mkt

class experiment2(object):
    def __init__(self):
        pass
    def author(self):
        return 'ycai330'
    def exp2(self, impact, sd, ed, symbol):
        sl = stratg.StrategyLearner(verbose = False, impact = impact, commission = 0.)
        sl.add_evidence(symbol = symbol, sd = sd, ed = ed, sv = 100000)
        trade = sl.testPolicy(symbol = symbol, sd = sd, ed = ed, sv = 100000)
        trade.columns = trade.columns.str.replace("Shares", 'Share')
        trade['Order'] = trade['Share'].apply(lambda x: 'BUY' if x>0 else 'SELL')
        trade['Symbol'] = symbol
        port = mkt.compute_portvals(trade, start_val = 100000, commission = 0., impact = impact)
        return port
    def main(self):
        impacts = [0., 0.0005, 0.01]
        sd=dt.datetime(2008, 1, 1)
        ed=dt.datetime(2009,12,31)
        symbol = 'JPM'
        ports = []
        for i in range(3):
            ports.append(self.exp2(impacts[i], sd, ed, symbol))
        crs = []
        dr = []
        nr = []
        stdR = []
        mdR = []
        for i in range(3):
            crs.append(ports[i][-1]/ports[i][0]-1.)
            dr.append(ports[i]/ports[i].shift(1)-1.)
            nr.append(ports[i]/ports[i][0]-1.)
            stdR.append(dr[i].std())
            mdR.append(dr[i].mean())
        
        # initialize
        plt.figure(figsize = (12,6), dpi = 120)
        
        # 
        plt.plot(nr[0], label = "0.", color = "green")
        # 
        plt.plot(nr[1], label = "0.0005", color = "red")
        # 
        plt.plot(nr[2], label = "0.01", color = "blue")
        # save
       
        plt.legend(loc = "upper left")
        plt.xlim(sd, ed)
        plt.xlabel("Date")
        plt.ylabel("Normalized Return")
        plt.tick_params(axis = "x", labelrotation = 45)
        plt.title("Impact Value")
        plt.savefig("exp2.png")
        
        plt.clf()
        
        print("")
        print("Cummulative Return impact = 0.0: ", crs[0])
        print("Cummulative Return impact = 0.0005: ", crs[1])
        print("Cummulative Rturn impact = 0.01: ", crs[2])
        print("")
        print("STD impact = 0.0: ", stdR[0])
        print("STD impact = 0.0005: ", stdR[1])
        print("STD impact = 0.01: ", stdR[2])
        print("")
        print("Mean impact = 0.0: ", mdR[0])
        print("Mean impact = 0.0005: ", mdR[1])
        print("Mean impact = 0.01: ", mdR[2])
        print("")

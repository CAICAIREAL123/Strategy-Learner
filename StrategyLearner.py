""""""  		  	   		  	  			  		 			     			  	 
"""  		  	   		  	  			  		 			     			  	 
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  	  			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  	  			  		 			     			  	 
All Rights Reserved  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  	  			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  	  			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  	  			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  	  			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  	  			  		 			     			  	 
or edited.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  	  			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  	  			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  	  			  		 			     			  	 
GT honor code violation.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		  	  			  		 			     			  	 
GT User ID: tb34 (replace with your User ID)  		  	   		  	  			  		 			     			  	 
GT ID: 900897987 (replace with your GT ID)  		  	   		  	  			  		 			     			  	 
"""  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
import datetime as dt  		  	   		  	  			  		 			     			  	 
import random  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    
import numpy as np
import BagLearner as bag
import RTLearner as rt
import indicators as ind
import ManualStrategy as manu
import math

import pandas as pd  		  	   		  	  			  		 			     			  	 
import util as ut  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
class StrategyLearner(object):  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    :param verbose: If ???verbose??? is True, your code can print out information for debugging.  		  	   		  	  			  		 			     			  	 
        If verbose = False your code should not generate ANY output.  		  	   		  	  			  		 			     			  	 
    :type verbose: bool  		  	   		  	  			  		 			     			  	 
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  	  			  		 			     			  	 
    :type impact: float  		  	   		  	  			  		 			     			  	 
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  	  			  		 			     			  	 
    :type commission: float  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    # constructor  		  	   		  	  			  		 			     			  	 
    def __init__(self, verbose=False, impact=0.005, commission=0.0):  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        Constructor method  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        self.verbose = verbose  		  	   		  	  			  		 			     			  	 
        self.impact = impact  		  	   		  	  			  		 			     			  	 
        self.commission = commission  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        # rt learner
        self.rtLearner = rt.RTLearner
        # bag learner
        self.bagLeafSize = 5
        self.bag = 20
        self.bagLearner = bag.BagLearner(self.rtLearner, kwargs = {"leaf_size":self.bagLeafSize}, bags = self.bag)
        self.n = 10
        self.windowSize = 20
        self.indicatorSize = 5
        
    # this method should create a QLearner, and train it for trading  		  	   		  	  			  		 			     			  	 
    def add_evidence(  		  	   		  	  			  		 			     			  	 
        self,  		  	   		  	  			  		 			     			  	 
        symbol="IBM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2008, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2009, 1, 1),  		  	   		  	  			  		 			     			  	 
        sv=10000,  		  	   		  	  			  		 			     			  	 
    ):  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        Trains your strategy learner over a given time frame.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        :param symbol: The stock symbol to train on  		  	   		  	  			  		 			     			  	 
        :type symbol: str  		  	   		  	  			  		 			     			  	 
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  	  			  		 			     			  	 
        :type sd: datetime  		  	   		  	  			  		 			     			  	 
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  	  			  		 			     			  	 
        :type ed: datetime  		  	   		  	  			  		 			     			  	 
        :param sv: The starting value of the portfolio  		  	   		  	  			  		 			     			  	 
        :type sv: int  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        # add your code to do learning here  		  	   		  	  			  		 			     			  	 
        thr = 0.0005+ self.impact
        #print(thr)
        #thr = 0.155 + self.impact # for out of sample data
        dateR = pd.date_range(sd, ed)
        dt = ut.get_data([symbol], dateR)[[symbol]]
        dt.dropna(inplace = True)
        #SMA
        sma = ind.sma(dt, symbol, lb = 2)
        price_sma = dt/sma
        price_sma = price_sma.rename(columns = {symbol:'sma'})
        #bollinger
        bbT, bbB = ind.bb(dt, [symbol], lb = 2)
        bbR = (dt - bbB)/(bbT - bbB)
        bbR = bbR.rename(columns = {symbol:'bbR'})
        #mm
        mm = ind.Momentum(dt, [symbol], lb = 2)
        mm = mm.rename(columns = {symbol:'mm'})
        
       
        indicator = pd.concat((price_sma, bbR, mm), axis = 1)
        indicator.dropna(inplace = True)
        indicator = indicator[:-5]
        #print(indicator)
        trainX = indicator.values
        trainY = []
        for i in range(len(dt)-5):
            #trainX.append(indicator.iloc[i])
            g = dt.iloc[i+5][symbol] - dt.iloc[i][symbol]
            g = g/dt.iloc[i][symbol]
            if g < -thr:
                trainY.append(-1)
            elif g>=-thr and g<=thr:
                trainY.append(0)
            else:
                trainY.append(1)
        #trainX = trainX[5 + self.windowSize + 1:len(dt)-self.n]
        trainY = np.array(trainY)
       # print(trainY)
        #trainX = trainX[self.n:,:]
        #print(trainX)
        #print(trainY)
        self.bagLearner.add_evidence(trainX, trainY)
        
  		  	   		  	  			  		 			     			  	 
        # example usage of the old backward compatible util function  		  	   		  	  			  		 			     			  	 
        #syms = [symbol]  		  	   		  	  			  		 			     			  	 
        #dates = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
        #prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		  	   		  	  			  		 			     			  	 
        #prices = prices_all[syms]  # only portfolio symbols  		  	   		  	  			  		 			     			  	 
        #prices_SPY = prices_all["SPY"]  # only SPY, for comparison later  		  	   		  	  			  		 			     			  	 
        #if self.verbose:  		  	   		  	  			  		 			     			  	 
            #print(prices)  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        # example use with new colname  		  	   		  	  			  		 			     			  	 
        #volume_all = ut.get_data(  		  	   		  	  			  		 			     			  	 
            #syms, dates, colname="Volume"  		  	   		  	  			  		 			     			  	 
        #)  # automatically adds SPY  		  	   		  	  			  		 			     			  	 
        #volume = volume_all[syms]  # only portfolio symbols  		  	   		  	  			  		 			     			  	 
        #volume_SPY = volume_all["SPY"]  # only SPY, for comparison later  		  	   		  	  			  		 			     			  	 
        #if self.verbose:  		  	   		  	  			  		 			     			  	 
            #print(volume)  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    # this method should use the existing policy and test it against new data  		  	   		  	  			  		 			     			  	 
    def testPolicy(  		  	   		  	  			  		 			     			  	 
        self,  		  	   		  	  			  		 			     			  	 
        symbol="IBM",  		  	   		  	  			  		 			     			  	 
        sd=dt.datetime(2009, 1, 1),  		  	   		  	  			  		 			     			  	 
        ed=dt.datetime(2010, 1, 1),  		  	   		  	  			  		 			     			  	 
        sv=10000,  		  	   		  	  			  		 			     			  	 
    ):  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
        Tests your learner using data outside of the training data  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        :param symbol: The stock symbol that you trained on on  		  	   		  	  			  		 			     			  	 
        :type symbol: str  		  	   		  	  			  		 			     			  	 
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  	  			  		 			     			  	 
        :type sd: datetime  		  	   		  	  			  		 			     			  	 
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  	  			  		 			     			  	 
        :type ed: datetime  		  	   		  	  			  		 			     			  	 
        :param sv: The starting value of the portfolio  		  	   		  	  			  		 			     			  	 
        :type sv: int  		  	   		  	  			  		 			     			  	 
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		  	  			  		 			     			  	 
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		  	  			  		 			     			  	 
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		  	  			  		 			     			  	 
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		  	  			  		 			     			  	 
        :rtype: pandas.DataFrame  		  	   		  	  			  		 			     			  	 
        """  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
        dateRange = pd.date_range(sd, ed)
        data = ut.get_data([symbol], dateRange)
        dt = data[[symbol]]
        dt.dropna(inplace = True)
        lb = 2
        
        #SMA
        sma = ind.sma(dt, symbol, lb = 2)
        price_sma = dt/sma
        price_sma = price_sma.rename(columns = {symbol:'sma'})
        #bollinger
        bbT, bbB = ind.bb(dt, [symbol], lb = 2)
        bbR = (dt - bbB)/(bbT - bbB)
        bbR = bbR.rename(columns = {symbol:'bbR'})
        #mm
        mm = ind.Momentum(dt, [symbol], lb = 2)
        mm = mm.rename(columns = {symbol:'mm'})
        
        indicator = pd.concat((price_sma, bbR, mm), axis = 1)
        indicator.fillna(0.,inplace = True)
        indicator.dropna(inplace = True)
        
        #print(indicator)
        
        
        testX = indicator.values
        
        #print(testX)
        testY = self.bagLearner.query(testX)
        #print(testY)
        trade = pd.DataFrame(0.,columns = ['Shares'], index = dt.index)
        count = 0
        for i in range(len(testY)-1):
            if count == 0:
                if testY[i]>0:
                    trade.iloc[i] = 1000.
                    count = 1
                elif testY[i]<0:
                    trade.iloc[i] = -1000.
                    count = -1
            elif count == 1:
                if testY[i]<0:
                    trade.iloc[i] = -2000.
                    count = -1
                elif testY[i]==0:
                    trade.iloc[i] = -1000.
                    count = 0
            else:
                if testY[i] > 0:
                    trade.iloc[i] = 2000.
                    count = 1
                elif testY[i]==0:
                    trade.iloc[i] = 1000.
                    count = 0
                
        if count == -1:
            trade.iloc[-1] = 1000.
        elif count == 1:
            trade.iloc[-1] = -1000.
        
       # print(trade)
        
        return  trade
        
            
            
        
        
        
        # here we build a fake set of trades  		  	   		  	  			  		 			     			  	 
        # your code should return the same sort of data  		  	   		  	  			  		 			     			  	 
        #dates = pd.date_range(sd, ed)  		  	   		  	  			  		 			     			  	 
        #prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		  	   		  	  			  		 			     			  	 
        #trades = prices_all[[symbol,]]  # only portfolio symbols  		  	   		  	  			  		 			     			  	 
        #trades_SPY = prices_all["SPY"]  # only SPY, for comparison later  		  	   		  	  			  		 			     			  	 
        #trades.values[:, :] = 0  # set them all to nothing  		  	   		  	  			  		 			     			  	 
        #trades.values[0, :] = 1000  # add a BUY at the start  		  	   		  	  			  		 			     			  	 
        #trades.values[40, :] = -1000  # add a SELL  		  	   		  	  			  		 			     			  	 
        #trades.values[41, :] = 1000  # add a BUY  		  	   		  	  			  		 			     			  	 
        #trades.values[60, :] = -2000  # go short from long  		  	   		  	  			  		 			     			  	 
        #trades.values[61, :] = 2000  # go long from short  		  	   		  	  			  		 			     			  	 
        #trades.values[-1, :] = -1000  # exit on the last day  		  	   		  	  			  		 			     			  	 
        #if self.verbose:  		  	   		  	  			  		 			     			  	 
            #print(type(trades))  # it better be a DataFrame!  		  	   		  	  			  		 			     			  	 
        #if self.verbose:  		  	   		  	  			  		 			     			  	 
        #    print(trades)  		  	   		  	  			  		 			     			  	 
        #if self.verbose:  		  	   		  	  			  		 			     			  	 
        #    print(prices_all)  		  	   		  	  			  		 			     			  	 
        #return trades  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    def author(self):
        return 'ycai330'
if __name__ == "__main__":  		  	   		  	  			  		 			     			  	 
    print("One does not simply think up a strategy")  		  	   		  	  			  		 			     			  	 

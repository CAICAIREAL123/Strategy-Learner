
""""""  		  	   		  	  			  		 			     			  	 
"""MC2-P1: Market simulator.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
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
import os  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
import numpy as np  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
import pandas as pd  		  	   		  	  			  		 			     			  	 
from util import get_data, plot_data  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 

## This code was reused. It was finished in the 2021 falls term and I dropped this class in the middle.	  	
def author(): 
    return 'ycai330' # replace tb34 with your Georgia Tech username. 


def compute_portvals(  		  	   		  	  			  		 			     			  	 
    orderFile,  		  	   		  	  			  		 			     			  	 
    start_val=100000,  		  	   		  	  			  		 			     			  	 
    commission=0.00, 	   		  	  			  		 			     			  	 
    impact=0.005,  		  	   		  	  			  		 			     			  	 
):  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    Computes the portfolio values.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    :param orders_file: Path of the order file or the file object  		  	   		  	  			  		 			     			  	 
    :type orders_file: str or file object  		  	   		  	  			  		 			     			  	 
    :param start_val: The starting value of the portfolio  		  	   		  	  			  		 			     			  	 
    :type start_val: int  		  	   		  	  			  		 			     			  	 
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		  	  			  		 			     			  	 
    :type commission: float  		  	   		  	  			  		 			     			  	 
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		  	  			  		 			     			  	 
    :type impact: float  		  	   		  	  			  		 			     			  	 
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		  	  			  		 			     			  	 
    :rtype: pandas.DataFrame  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    # this is the function the autograder will call to test your code  		  	   		  	  			  		 			     			  	 
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		  	  			  		 			     			  	 
    # code should work correctly with either input  		  	   		  	  			  		 			     			  	 
    # TODO: Your code here  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    # In the template, instead of computing the value of the portfolio, we just  		  	   		  	  			  		 			     			  	 
    # read in the value of IBM over 6 months  		  	   		  	  			  		 			     			  	 
    #start_date = dt.datetime(2008, 1, 1)  		  	   		  	  			  		 			     			  	 
    #end_date = dt.datetime(2008, 6, 1)  		  	   		  	  			  		 			     			  	 
    #portvals = get_data(["IBM"], pd.date_range(start_date, end_date))  		  	   		  	  			  		 			     			  	 
    #portvals = portvals[["IBM"]]  # remove SPY  		  	   		  	  			  		 			     			  	 
    #rv = pd.DataFrame(index=portvals.index, data=portvals.values)  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    #return rv  		  	   		  	  			  		 			     			  	 
    #return portvals  		  	   		  	  			  		 			     			  	 
    #open file
    #orderFile = pd.read_csv(orders_file, index_col = "Date", parse_dates = True, na_values = ['nan']).sort_index()
    #get symbols
    
    #orderFile['Share'] = abs(orderFile['Share'])
    symbols = list(set(orderFile['Symbol'].values))
    #symbols.append('CASH')
    #get date
    startDate = orderFile.index.min()
    endDate = orderFile.index.max()
    dates = pd.date_range(startDate, endDate)
    #add buy flag
    orderFile['BuyorSell'] = orderFile['Order'].apply(lambda x: 1 if x == 'BUY' else -1)
    #orderFile.to_csv('orders.csv', index = False)
    #build price form
    prices = get_data(symbols,dates, addSPY = False)
    prices.fillna(method = 'bfill', inplace = True)
    prices.fillna(method = 'ffill', inplace = True)
    #add cash column
    prices['Cash'] = 1.0
    symbols.append('Cash')
    #set up trade form
    t = pd.DataFrame(index = dates, columns = symbols, dtype = float)        
    t = t.fillna(0)
    #initial start value
    t.loc[startDate,'Cash'] += start_val
    #calculate price
    for d, r in orderFile.iterrows():
        s = r['Symbol']#symble
        sh = abs(r['Share'])#shares
        flag = r['BuyorSell']#flag
        p = prices[s][d]#price
        t[s][d] += sh * flag
        t.loc[d,'Cash'] += commission - flag * sh * p * (1 + flag * impact)
    portvals = np.cumsum(t, axis = 0) * prices
    return np.sum(portvals, axis = 1)
    
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
def test_code():  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    Helper function to test code  		  	   		  	  			  		 			     			  	 
    """  		  	   		  	  			  		 			     			  	 
    # this is a helper function you can use to test your code  		  	   		  	  			  		 			     			  	 
    # note that during autograding his function will not be called.  		  	   		  	  			  		 			     			  	 
    # Define input parameters  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    of = "./orders/orders2.csv"  		  	   		  	  			  		 			     			  	 
    sv = 1000000  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    # Process orders  		  	   		  	  			  		 			     			  	 
    portvals = compute_portvals(orders_file=of, start_val=sv)  		  	   		  	  			  		 			     			  	 
    if isinstance(portvals, pd.DataFrame):  		  	   		  	  			  		 			     			  	 
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		  	  			  		 			     			  	 
    else:  		  	   		  	  			  		 			     			  	 
        "warning, code did not return a DataFrame"  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    # Get portfolio stats  		  	   		  	  			  		 			     			  	 
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		  	  			  		 			     			  	 
    start_date = dt.datetime(2008, 1, 1)  		  	   		  	  			  		 			     			  	 
    end_date = dt.datetime(2008, 6, 1)  		  	   		  	  			  		 			     			  	 
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [  		  	   		  	  			  		 			     			  	 
        0.2,  		  	   		  	  			  		 			     			  	 
        0.01,  		  	   		  	  			  		 			     			  	 
        0.02,  		  	   		  	  			  		 			     			  	 
        1.5,  		  	   		  	  			  		 			     			  	 
    ]  		  	   		  	  			  		 			     			  	 
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [  		  	   		  	  			  		 			     			  	 
        0.2,  		  	   		  	  			  		 			     			  	 
        0.01,  		  	   		  	  			  		 			     			  	 
        0.02,  		  	   		  	  			  		 			     			  	 
        1.5,  		  	   		  	  			  		 			     			  	 
    ]  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
    # Compare portfolio against $SPX  		  	   		  	  			  		 			     			  	 
    print(f"Date Range: {start_date} to {end_date}")  		  	   		  	  			  		 			     			  	 
    print()  		  	   		  	  			  		 			     			  	 
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		  	  			  		 			     			  	 
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		  	  			  		 			     			  	 
    print()  		  	   		  	  			  		 			     			  	 
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		  	  			  		 			     			  	 
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		  	  			  		 			     			  	 
    print()  		  	   		  	  			  		 			     			  	 
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		  	  			  		 			     			  	 
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		  	  			  		 			     			  	 
    print()  		  	   		  	  			  		 			     			  	 
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		  	  			  		 			     			  	 
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		  	  			  		 			     			  	 
    print()  		  	   		  	  			  		 			     			  	 
    print(f"Final Portfolio Value: {portvals[-1]}")  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
if __name__ == "__main__":  		  	   		  	  			  		 			     			  	 
    test_code()  	
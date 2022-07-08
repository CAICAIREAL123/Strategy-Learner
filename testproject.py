import ManualStrategy
import numpy as np
import pandas as pd
import datetime as dt
import util as ut
import matplotlib.pyplot as plt
import indicators as ind
import marketsimcode as mkt
import StrategyLearner as stratg
import experiment1 as exp1
import experiment2 as exp2

if __name__ == "__main__":
    ManualStrategy.main()
    exp1.main()
    e2 = exp2.experiment2()
    e2.main()
    

# This code was reused from last term.
import numpy as np

class BagLearner(object):
    def __init__(self, learner, kwargs = {}, boost = False, bags = 20, verbose = False):
        self.learners = []
        self.learner = learner
        self.bags = bags
        self.kwargs = kwargs
        self.boost = boost
        for i in range(bags):
            self.learners.append(learner(**kwargs))
         
    def author(self):
        return "ycai330"
    
    def add_evidence(self, data_x, data_y): 
        for l in self.learners:
            index = np.random.choice(data_x.shape[0],data_x.shape[0], replace=True)
            l.add_evidence(data_x[index], data_y[index])
            
    def query(self, points): 
        output = []
        for l in self.learners:
            q = l.query(points)
            output.append(q)
        #if self.verbose:
            #print(output)
        return np.mean(np.asarray(output), axis = 0)
    
if __name__ == "__main__": 
    print("")  
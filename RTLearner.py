
# This code was reused from last term.
import numpy as np 


class RTLearner(object): 
    
    def __init__(self, verbose=False, leaf_size = 1):
        self.verbose = verbose
        self.leaf_size = leaf_size
        self.tree = None
        self.queryResult = None
        
    def author(self):  
        return "ycai330"

    def add_evidence(self, data_x, data_y): 
        data_y = data_y.reshape(-1, 1)
        data = np.hstack((data_x, data_y))
        self.tree = self.buildTree(data) 
        
        
    def query(self, points): 
        output = np.array([])
        for x in points:
            count = 0
            flag = True
            while flag:
                index = int(self.tree[count][0])
                split = self.tree[count][1]
                if index == -1:
                    flag = False
                    output = np.append(output, split)
                else:
                    if x[index] <= split:
                        count = int(count + self.tree[count][2])
                    else:
                        count = int(count + self.tree[count][3])
        return output
    
    def searchFeat(self, mode, data, features):
        output = None
        if mode == "random":
            output = np.random.randint(0, data.shape[1]-2)
        else:
            output = np.random.randint(len(features[0]))
        return output
    
    def searchSplit(self, data_x, data_y):
        x = len(data_x)
        rand1 = np.random.randint(x)
        rand2 = np.random.randint(x)
        output = (data_x[rand1, self.searchFeat("random", data_x, data_y, None)] + data_x[rand2, self.searchFeat("random", data_x, data_y, None)])/2
        return output
    
    def buildTree(self, data):
        dataL = data.shape[0]
        if dataL <= self.leaf_size or (data[:, -1] ==data[0, -1]).all():
            return np.array([[-1, np.mean(data[:,-1]), -1, -1]])
        else:
            bestFeat = self.searchFeat("random", data, None)
            split = np.median(data[:,bestFeat])
            dataUnFeat = data[data[:,bestFeat]>split]
            dataFeat = data[data[:,bestFeat]<=split]
            if dataFeat.shape[0] == 0 or dataUnFeat.shape[0] == 0:
                return np.array([[-1, np.mean(data[:,-1]), -1, -1]])
            else:
                leftTree = self.buildTree(dataFeat)
                rightTree = self.buildTree(dataUnFeat)
                root = np.array([bestFeat, split, 1, leftTree.shape[0]+1])
                return np.vstack([root, leftTree,rightTree])

if __name__ == "__main__": 
    print("")  
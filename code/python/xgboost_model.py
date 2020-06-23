# libs
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier 
from xgboost import plot_tree
import matplotlib.pyplot as plt


class xgboost_model:
    """
    docstring 
    """
    
    ### constructor 
    def __init__ (self):
        self.OutputFolder = "."     # default is pwd
    
    ### setter methods
    def setOutputFolder(self, OutputFolder):
        # set OutputFolder as a class level variable
        self.OutputFolder = OutputFolder
        
        # create the directory if it doesn't exist 
        if not os.path.exists(OutputFolder):
            os.makedirs(OutputFolder)
        
    ### getter methods
    def getOutputFolder(self):
        return self.OutputFolder
    
    ### modeling functions 
    def TrainModel(self, x, y, model_name):
        # split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)
        
        # xgboost training 
        model = XGBClassifier()
        model.fit(X_train,y_train)
        
        # xgboost testing
        y_pred = model.predict(X_test)
        predictions = [round(value) for value in y_pred]
        
        # evaluate predictions
        accuracy = accuracy_score(y_test, predictions)
        print("Accuracy: %.2f%%" % (accuracy * 100.0))
                
        # return 
        return model
    
    def PlotModelTree(self, model, model_name):
        # plot tree
        plot_tree(model, rankdir='LR')
        fig = plt.gcf()
        fig.set_size_inches(150, 100)
        fig.savefig(self.getOutputFolder()+'/tree_'+model_name+'.png')
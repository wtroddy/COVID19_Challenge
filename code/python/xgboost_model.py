# libs
import os
import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from xgboost import XGBClassifier 
from xgboost import plot_tree
from xgboost import plot_importance
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
    def TrainEvalModel(self, x, y, model_name):
        # split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)
        
        ### xgboost training 
        model = XGBClassifier(max_depth = 10, learning_rate = 0.05)
        model.fit(X_train, y_train)
        
        ### xgboost testing
        y_pred = model.predict(X_test)
        predictions = [round(value) for value in y_pred]
        
        ### evaluate predictions
        # accuracy
        accuracy = accuracy_score(y_test, predictions)
        print("Accuracy: %.2f%%" % (accuracy * 100.0))
        
        ### probability 
        y_pred_proba = model.predict_proba(X_test)
        y_pred_proba_pos = y_pred_proba[:, 1]
        
        # roc auc score        
        #auc = roc_auc_score(y_test, y_pred_proba_pos)
        #print("ROC AUC=%.3f" % (auc))
        
        # calc roc curve        
        #fpr, tpr, _ = roc_curve(y_test, y_pred_proba_pos)
        
        # plot ROC curve
        #plt.plot(fpr, tpr)
        #plt.xlabel('Flase Positive Rate')
        #plt.ylabel('True Positive Rate')
        #plt.savefig(self.getOutputFolder()+'/roc_curve.png')
        
        # output scores
        f = open(self.getOutputFolder()+"/scores.txt", "a")
        f.write("\n")
        f.write(datetime.datetime.now().strftime("%c"))
        f.write("\n")
        f.write(str(model.evals_result))
        f.write("\n")
        f.write("Accuracy: %.2f%%" % (accuracy * 100.0))
        f.write("\n")
        #f.write("ROC AUC=%.3f" % (auc))
        #f.write("\n")
        f.close()

        # return 
        return model
    
    ### Model Tree Plotter
    def PlotModelTree(self, model, model_name):
        # plot tree
        plot_tree(model, rankdir='LR')
        fig = plt.gcf()
        fig.set_size_inches(25, 15)
        fig.savefig(self.getOutputFolder()+'/model_tree.png')
        # plot importances
        plot_importance(model)
        fig = plt.gcf()
        fig.set_size_inches(25, 25)
        fig.savefig(self.getOutputFolder()+'/feat_importances.png')
        
        
    
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier 
from xgboost import plot_tree
import matplotlib.pyplot as plt

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.9)
        
# xgboost training 
model = XGBClassifier()
eval_set = [(X_test, y_test)]
model.fit(X_train,y_train, eval_metric = ["error", "rmse"], eval_set = eval_set)

# xgboost testing
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]

# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

### probability 
y_pred_proba = model.predict_proba(X_test)
y_pred_proba_pos = y_pred_proba[:, 1]

# roc auc score
from sklearn.metrics import roc_auc_score
auc = roc_auc_score(y_test, y_pred_proba_pos)
print('ROC AUC=%.3f' % (auc))

# calc roc curve
from sklearn.metrics import roc_curve
fpr, tpr, _ = roc_curve(y_test, y_pred_proba_pos)

# print metrics
print('FPR=%.3f' % (fpr))
print('TPR=%.3f' % (tpr))

# plot roc curve
plt.plot(fpr, tpr)
#plt.plot(fpr)
#plt.plot(tpr)

##############################################################################
##############################################################################
##############################################################################
##############################################################################

# xgboost training 
model = XGBClassifier()
model.fit(train_x, train_y)
probs = model.predict_proba(test_x)


# probs
import statistics as s
s.median(probs[0])
s.median(probs[1])







from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

def validate(estimator=None, param_grid=None, folds=1000):
    '''
    Validates a classifier using StratifiedShuffleSplit() 
        
    Metrics include: F1-score, recall, and percision
       
    Args:
        clf: a SkLearn classifier
        labels_df: PD_dataframe of labels to predict.
        features_df: PD_dataframe of features used to predict labels.
        n_iter: Number of random cross validation runs to average over.
        test_size: The percentage size of the test set to split off during each
            run.
    Returns:
        Prints to stdout the evaluation average evaluation metrics for F1
            score, recall, and precission.
    '''

    # param_dict = {}

    # cv = StratifiedShuffleSplit(labels, folds, random_state = 42)
    # clf = GridSearchCV(pipeline, param_dict, cv=cv)
    # clf.fit()




    n_iter = 1000
    sk_fold = StratifiedShuffleSplit(labels_df, n_iter=n_iter, test_size=0.1)
    f1_avg = []
    recall_avg = []
    precision_avg = []
    # Enumerate through the cross-validation splits get an index i for a timer
    for i, all_index in enumerate(sk_fold):
        train_index = all_index[0]
        test_index = all_index[1]

        X_train = features_df.irow(train_index)
        y_train = labels_df[train_index]
        
        X_test = features_df.irow(test_index)        
        y_test = labels_df[test_index]
        
        # Use the best estimator trained earlier to fit
        # grid_search_object.best_estimator_.fit(X_train, y=y_train)
        test_pred = clf.predict(X_test)
        
        # Each time i is divsible by 10, print the 10% to console.
        if i % round(n_iter/10) == 0:
            sys.stdout.write('{0}%.. '.format(float(i)/n_iter*100)) 
            sys.stdout.flush()        
        f1_avg.append(f1_score(y_test, test_pred))
        precision_avg.append(precision_score(y_test, test_pred))
        recall_avg.append(recall_score(y_test, test_pred))
    
    print "Done!"
    print ""
    print "F1 Avg: ", sum(f1_avg)/n_iter
    print "Precision Avg: ", sum(precision_avg)/n_iter
    print "Recall Avg: ", sum(recall_avg)/n_iter







#####################################################################
#####################################################################
##################### Tester Code to Build From #####################
#####################################################################
#####################################################################



# import pickle
# import sys
# from sklearn.cross_validation import StratifiedShuffleSplit
# sys.path.append("../tools/")
# from feature_format import featureFormat, targetFeatureSplit

# PERF_FORMAT_STRING = "\
# \tAccuracy: {:>0.{display_precision}f}\tPrecision: {:>0.{display_precision}f}\t\
# Recall: {:>0.{display_precision}f}\tF1: {:>0.{display_precision}f}\tF2: {:>0.{display_precision}f}"
# RESULTS_FORMAT_STRING = "\tTotal predictions: {:4d}\tTrue positives: {:4d}\tFalse positives: {:4d}\
# \tFalse negatives: {:4d}\tTrue negatives: {:4d}"

# def test_classifier(clf, dataset, feature_list, folds = 1000):
#     print feature_list # I added this line to print features list to ml_results.txt
#     data = featureFormat(dataset, feature_list, sort_keys = True)
#     labels, features = targetFeatureSplit(data)
#     cv = StratifiedShuffleSplit(labels, folds, random_state = 42)
#     true_negatives = 0
#     false_negatives = 0
#     true_positives = 0
#     false_positives = 0
#     for train_idx, test_idx in cv: 
#         features_train = []
#         features_test  = []
#         labels_train   = []
#         labels_test    = []
#         for ii in train_idx:
#             features_train.append( features[ii] )
#             labels_train.append( labels[ii] )
#         for jj in test_idx:
#             features_test.append( features[jj] )
#             labels_test.append( labels[jj] )
        
#         ### fit the classifier using training set, and test on test set
#         clf.fit(features_train, labels_train)

#         # print "BEGIN: SelectKBest Info..."
#         # print select.clf.scores_
#         # print clf.pvalues_
#         # print clf.get_support
#         # print clf.get_params
#         # print "END: SelectKBest Info..."


#         predictions = clf.predict(features_test)
#         for prediction, truth in zip(predictions, labels_test):
#             if prediction == 0 and truth == 0:
#                 true_negatives += 1
#             elif prediction == 0 and truth == 1:
#                 false_negatives += 1
#             elif prediction == 1 and truth == 0:
#                 false_positives += 1
#             elif prediction == 1 and truth == 1:
#                 true_positives += 1
#             else:
#                 print "Warning: Found a predicted label not == 0 or 1."
#                 print "All predictions should take value 0 or 1."
#                 print "Evaluating performance for processed predictions:"
#                 break
#     try:
#         total_predictions = true_negatives + false_negatives + false_positives + true_positives
#         accuracy = 1.0*(true_positives + true_negatives)/total_predictions
#         precision = 1.0*true_positives/(true_positives+false_positives)
#         recall = 1.0*true_positives/(true_positives+false_negatives)
#         f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
#         f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
#         print clf
#         print PERF_FORMAT_STRING.format(accuracy, precision, recall, f1, f2, display_precision = 5)
#         print RESULTS_FORMAT_STRING.format(total_predictions, true_positives, false_positives, false_negatives, true_negatives)
#         print ""
#     except:
#         print "Got a divide by zero when trying out:", clf
#         print "Precision or recall may be undefined due to a lack of true positive predicitons."






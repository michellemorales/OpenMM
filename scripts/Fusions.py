#!/usr/bin/env python

""" This is module for performing different multimodal fusion experiments """
import pandas
import numpy as np
from sklearn import svm
from sklearn.preprocessing import Imputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, accuracy_score, classification_report



def early_fusion(multimodal_files):
    """
    This function fuses unimodal data files into one multimodal csv file
    :param multimodal_files: a list of unimodal csv files
    :param write2file: file name to write data to
    :return: mm_names, mm_feats
        WHERE
        list mm_names is the feature names
        list mm_feats is a list of feature lists
    """
    # Statistics we will use to combine features at the frame/sentence level to the participant level
    stats_names = ['max', 'min', 'mean', 'median', 'std']
    mm_feats = []
    mm_names = []
    # Process each unimodal data file
    print('Processing unimodal files...\n')
    for feat_file in multimodal_files:
        df = pandas.read_csv(feat_file, header='infer')
        feature_names = df.columns.values
        for feat in feature_names:
            # Feature vector
            vals = df[feat].values
            # Run statistics
            maximum = np.nanmax(vals)
            minimum = np.nanmin(vals)
            mean = np.nanmean(vals)
            median = np.nanmedian(vals)
            std = np.nanstd(vals)
            names = [feat.strip() + "_" + stat for stat in stats_names]
            feats = [maximum, minimum, mean, median, std]
            for n in names:
                mm_names.append(n)
            for f in feats:
                mm_feats.append(f)
    print('Done combining modalities!\n')
    return mm_names, mm_feats


def predict_regression(train_data, test_data, train_labels, test_labels):
    """
    This function predicts depression score using an SVM regression algorithm (SVR - http://scikit-learn.org/stable/modules/svm.html#regression)

    :param train_data: list of feature lists for training data
    :param train_labels: list of depression score labels for training data
    :param test_data: list of feature lists for test data
    :param test_labels: list of depression score labels for test data
    :return: MAE, RMSE
        WHERE
        float MAE is mean absolute error
        float RMSE is root mean square error
    """
    # Handle missing data in train
    # missing_values is the value of your placeholder, strategy is if you'd like mean, median or mode, and axis=0 means it calculates the imputation based on the other feature values for that sample
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imp.fit(train_data)
    train_imp = imp.transform(train_data)

    # Handle missing data in dev
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imp.fit(test_data)
    test_imp = imp.transform(test_data)

    clf = svm.SVR()
    clf.fit(train_imp, train_labels)
    predictions = clf.predict(test_imp)
    MAE = mean_absolute_error(predictions, test_labels)
    RMSE = mean_squared_error(predictions, test_labels) ** 0.5
    return MAE, RMSE


def predict_class(train_data, test_data, train_labels, test_labels):
    """
    This function predicts depression class (depressed/not depressed) using an SVM classification algorithm (SVC - http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC )

    :param train_data: list of feature lists for training data
    :param train_labels: list of depression (binary) class labels for training data
    :param test_data: list of feature lists for test data
    :param test_labels: list of depression (binary) class labels for test data
    :return: accuracy
        WHERE
        float accuracy is the percentage of correct predictions
    """
    # Handle missing data in train
    # missing_values is the value of your placeholder, strategy is if you'd like mean, median or mode, and axis=0 means it calculates the imputation based on the other feature values for that sample
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imp.fit(train_data)
    train_imp = imp.transform(train_data)

    # Handle missing data in dev
    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    imp.fit(test_data)
    test_imp = imp.transform(test_data)

    clf = svm.SVC()
    clf.fit(train_imp, train_labels)
    predictions = clf.predict(test_imp)
    accuracy = accuracy_score(test_labels, predictions)
    print(classification_report(test_labels, predictions))
    return accuracy


# def late_fusion_regression():

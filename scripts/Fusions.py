#!/usr/bin/env python

""" This is module for performing different multimodal fusion experiments """
import pandas
import scipy.stats
import numpy as np
from sklearn import svm
from sklearn.metrics import mean_squared_error


def early_fusion(multimodal_files):
    """
    This function fuses unimodal data files into one multimodal csv file
    :param multimodal_files: a list of unimodal csv files
    :return: mm_names, mm_feats
        WHERE
        list mm_names is the feature names
        list mm_feats is a list of feature lists
    """
    # Statistics we will use to combine features at the frame/sentence level to the participant level
    stats_names = ['max', 'min', 'mean', 'median', 'std', 'var', 'kurt', 'skew', 'percentile25', 'percentile50',
                   'percentile75']
    mm_feats = []
    mm_names = []
    # Process each unimodal data file
    print('Processing unimodal files...')
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
            var = np.nanvar(vals)
            kurt = scipy.stats.kurtosis(vals)
            skew = scipy.stats.skew(vals)
            percentile25 = np.nanpercentile(vals, 25)
            percentile50 = np.nanpercentile(vals, 50)
            percentile75 = np.nanpercentile(vals, 75)
            names = [feat.strip() + "_" + stat for stat in stats_names]
            feats = [maximum, minimum, mean, median, std, var, kurt, skew, percentile25, percentile50, percentile75]
            for n in names:
                mm_names.append(n)
            for f in feats:
                mm_feats.append(f)
    print('Done combining modalities!')
    return mm_names, mm_feats


def predict_regression(train_data, test_data, train_labels, test_labels):
    """
    This function predicts depression score using an SVM regression algorithm (SVR - http://scikit-learn.org/stable/modules/svm.html#regression)

    :param train_data: list of feature lists for training data
    :param train_labels: list of depression score labels for training data
    :param test_data: list of feature lists for test data
    :param test_labels: list of depression score labels for test data
    :return: RMSE
        WHERE
        float RMSE is root mean square error
    """
    clf = svm.SVR()
    clf.fit(train_data, train_labels)
    predictions = clf.predict(test_data)
    RMSE = mean_squared_error(predictions, test_labels) ** 0.5
    return RMSE


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


if __name__ == "__main__":
    print('Running fusion experiments...')
    # TODO:

    # Get data for all participants

    # Perform early fusion

    # Experimental Set-up : train on train-split.csv and test of dev_split.csv

    # Get depression labels for each participant from splits

    # Perform regression experiments

    # Perform classification experiments
    print('Done!')

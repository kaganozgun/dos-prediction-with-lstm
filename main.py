#  Copyright (c) 2023. Kağan Özgün ITU Computer Engineering

SEED = 123456
import os
import random as rn
import numpy as np
import tensorflow
import argparse

from cicdos2019.lstm.data_prep import prepare_cicdos2019_all_dataset
from cicdos2019.lstm.test import cicddos2019_test
from cicdos2019.lstm.train import cicddos2019_train_lstm_model
from cicdos2019.rulebased.rule_based import calculate_rule_based_cicddos2019
from cicdos2019.gaussiannaivebayes.gnb import cicddos2019_gaussian_naive_bayes

from unswnb15.rulebased.rule_based import calculate_rule_based_unswnb15
from unswnb15.lstm.data_prep import prepare_unsw_nb_15_all_dataset
from unswnb15.gaussiannaivebayes.gnb import unswnb15_gaussian_naive_bayes
from unswnb15.lstm.train import train_lstm_model
from unswnb15.lstm.test import test

os.environ['PYTHONHASHSEED'] = str(SEED)
np.random.seed(SEED)
tensorflow.random.set_seed(SEED)
rn.seed(SEED)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', type=str, help='Chose dataset')
    parser.add_argument('-m', '--model', type=str, help='Chose model')

    args = parser.parse_args()

    if args.model == 'lstm':
        if args.dataset == 'unswnb15':
            base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/UNSW-NB15"
            prepare_unsw_nb_15_all_dataset(base_path)
            #base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/UNSW-NB15/lstm_prediction/data_prep"
            #train_lstm_model(base_path)
            test()
        elif args.dataset == 'cicddos2019':
            base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/CIC-DDoS2019"
            prepare_cicdos2019_all_dataset(base_path)
            base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/CIC-DDoS2019/lstm_prediction/data_prep"
            cicddos2019_train_lstm_model(base_path)
            cicddos2019_test()
        else:
            print("Unknow dataset")
    elif args.model == 'gnb':
        if args.dataset == 'unswnb15':
            base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/UNSW-NB15/lstm_prediction/data_prep"
            unswnb15_gaussian_naive_bayes(base_path)
        elif args.dataset == 'cicddos2019':
            base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/CIC-DDoS2019/lstm_prediction/data_prep"
            cicddos2019_gaussian_naive_bayes(base_path)
        else:
            print("Unknow dataset")
    elif args.model == 'rule-based':
        if args.dataset == 'unswnb15':
            base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/UNSW-NB15"
            calculate_rule_based_unswnb15(base_path)
        elif args.dataset == 'cicddos2019':
            base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/CIC-DDoS2019"
            calculate_rule_based_cicddos2019(base_path, 0.3)
        else:
            print("Unknow dataset")
    else:
        print("Unknow model")


if __name__ == "__main__":
    main()

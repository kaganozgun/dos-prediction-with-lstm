#  Copyright (c) 2023. Kağan Özgün ITU Computer Engineering

import os
import random as rn
import numpy as np
import tensorflow
import argparse

from cicddos2019.lstm.test import cicddos2019_test
from cicddos2019.dataprep.data_prep import prepare_cicddos2019_all_dataset
from cicddos2019.lstm.train import cicddos2019_train_lstm_model
from cicddos2019.rulebased.rule_based import calculate_rule_based_cicddos2019
from cicddos2019.gaussiannaivebayes.gnb import cicddos2019_gaussian_naive_bayes

from unswnb15.rulebased.rule_based import calculate_rule_based_unswnb15
from unswnb15.dataprep.data_prep import prepare_unsw_nb_15_all_dataset
from unswnb15.gaussiannaivebayes.gnb import unswnb15_gaussian_naive_bayes
from unswnb15.lstm.train import unswnb15_train_lstm_model
from unswnb15.lstm.test import unswnb15_test

SEED = 123456
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
            base_path = "unswnb15/dataset/processed"
            unswnb15_train_lstm_model(base_path)
            unswnb15_test(base_path)
        elif args.dataset == 'cicddos2019':
            base_path = "cicddos2019/dataset/processed"
            cicddos2019_train_lstm_model(base_path)
            cicddos2019_test(base_path)
        else:
            print("Unknow dataset")
    elif args.model == 'gnb':
        if args.dataset == 'unswnb15':
            base_path = "unswnb15/dataset/processed"
            unswnb15_gaussian_naive_bayes(base_path)
        elif args.dataset == 'cicddos2019':
            base_path = "cicddos2019/dataset/processed"
            cicddos2019_gaussian_naive_bayes(base_path)
        else:
            print("Unknow dataset")
    elif args.model == 'rule-based':
        if args.dataset == 'unswnb15':
            input_path = "unswnb15/dataset/raw"
            calculate_rule_based_unswnb15(input_path)
        elif args.dataset == 'cicddos2019':
            input_path = "cicddos2019/dataset/raw"
            calculate_rule_based_cicddos2019(input_path, 0.3)
        else:
            print("Unknow dataset")
    elif args.model == 'data-prep':
        if args.dataset == 'unswnb15':
            prepare_unsw_nb_15_all_dataset()
        elif args.dataset == 'cicddos2019':
            prepare_cicddos2019_all_dataset()
        else:
            print("Unknow dataset")
    else:
        print("Unknow model")


if __name__ == "__main__":
    main()

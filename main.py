#  Copyright (c) 2023. Kağan Özgün ITU Computer Engineering
from data_prep import prepare_unsw_nb_15_all_dataset
from train import train_lstm_model
from test import test


def main():
    #base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/UNSW-NB15"
    #prepare_unsw_nb_15_all_dataset(base_path)
    #base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/UNSW-NB15/lstm_prediction/data_prep"
    #train_lstm_model(base_path)
    test()


if __name__ == "__main__":
    main()

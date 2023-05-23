#  Copyright (c) 2023. Kağan Özgün ITU Computer Engineering

import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report


def test():
    result_df = pd.DataFrame()
    for data_type in ["srcip-dport", "dstip-dport"]:
        for split_shape in ["60-20-20", "60-10-30", "70-30"]:
            for window_1 in [20, 50, 100, 200]:
                for window_2 in [300, 600, 1200, 1800, 2400, 3000]:
                    base_path = "/Users/kagan.ozgun/Desktop/YL/Tez/UNSW-NB15/lstm_prediction/data_prep/" + data_type \
                                + "/" + split_shape + "/w" + str(window_1) + "_p" + str(window_2)
                    X_test = np.load(f"{base_path}/x_test_data.npy")
                    y_test = np.load(f"{base_path}/y_test_data.npy")
                    y_test = y_test.reshape(-1)

                    model = load_model(f"{base_path}/final.h5")
                    y_pred = np.round(model.predict(X_test)).flatten()
                    report = classification_report(y_test, y_pred,output_dict=True)

                    df_tmp = pd.DataFrame({'test_shape': split_shape,
                              'data_type': data_type, 'win_1': window_1, 'win_2': window_2,
                              'pred_sec': window_2 / 10,
                              'test_data_size': len(y_test),
                              'accuracy': report["accuracy"],
                              'recall_0': report["0.0"]["recall"],
                              'recall_1': report["1.0"]["recall"],
                              'precision_0': report["0.0"]["precision"],
                              'precision_1': report["1.0"]["precision"],
                              'f1_score_0': report["0.0"]["f1-score"],
                              'f1_score_1': report["1.0"]["f1-score"]}, index=[0])
                    result_df = pd.concat([result_df, df_tmp], ignore_index = True)

    datatoexcel = pd.ExcelWriter('lstm-srcip-dport.xlsx')
    result_df.to_excel(datatoexcel)
    datatoexcel.book.save('lstm-unswbn15-results.xlsx')

import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report


def unswnb15_gaussian_naive_bayes(base_path):
    result_df = pd.DataFrame()
    for t in ["srcip-dport", "dstip-dport"]:
        print(f"\t\t\tType: {t}")
        for window_1 in [20, 50, 100, 200]:
            print(f"\tWindow 1: {window_1}")
            for window_2 in [300, 600, 1200, 1800, 2400, 3000]:
                print(f"\t\tWindow 2: {window_2}")
                path = base_path + "/" + t + "/70-30/w" + str(window_1) + "_p" + str(window_2)
                x_train = np.load(f"{path}/x_train_data.npy")
                x_train_raw_shape = x_train.shape
                x_train = np.reshape(x_train, (x_train_raw_shape[0], x_train_raw_shape[1] * x_train_raw_shape[2]))

                x_test = np.load(f"{path}/x_test_data.npy")
                x_test_raw_shape = x_test.shape
                x_test = np.reshape(x_test, (x_test_raw_shape[0], x_test_raw_shape[1] * x_test_raw_shape[2]))

                y_train = np.load(f"{path}/y_train_data.npy")
                y_train = y_train.reshape(-1)

                y_test = np.load(f"{path}/y_test_data.npy")
                y_test = y_test.reshape(-1)

                clf = GaussianNB()
                clf.fit(x_train, y_train)
                prob = clf.predict_proba(x_test)

                pred = clf.predict(x_test)

                level_1 = []
                level_2 = []
                for _, p in prob:
                    if p <= 0.5:
                        level_1.append(0)
                        level_2.append(0)
                    elif p <= 0.75:
                        level_1.append(1)
                        level_2.append(0)
                    else:
                        level_1.append(1)
                        level_2.append(1)

                report = classification_report(y_test, level_1, output_dict=True)
                report_2 = classification_report(y_test, level_2, output_dict=True)

                df_tmp = pd.DataFrame({'test_shape': '70-30',
                                       'data_type': t,
                                       'win_1': window_1,
                                       'win_2': window_2,
                                       'pred_sec': window_2 / 10,
                                       'test_data_size': len(y_test),
                                       'accuracy_lvl_1': report["accuracy"],
                                       'recall_0_lvl_1': report["0.0"]["recall"],
                                       'recall_1_lvl_1': report["1.0"]["recall"],
                                       'precision_0_lvl_1': report["0.0"]["precision"],
                                       'precision_1_lvl_1': report["1.0"]["precision"],
                                       'f1_score_0_lvl_1': report["0.0"]["f1-score"],
                                       'f1_score_1_lvl_1': report["1.0"]["f1-score"],
                                       'accuracy_lvl_2': report_2["accuracy"],
                                       'recall_0_lvl_2': report_2["0.0"]["recall"],
                                       'recall_1_lvl_2': report_2["1.0"]["recall"],
                                       'precision_0_lvl_2': report_2["0.0"]["precision"],
                                       'precision_1_lvl_2': report_2["1.0"]["precision"],
                                       'f1_score_0_lvl_2': report_2["0.0"]["f1-score"],
                                       'f1_score_1_lvl_2': report_2["1.0"]["f1-score"]}, index=[0])
                result_df = pd.concat([result_df, df_tmp], ignore_index=True)

    path = 'results/unswbn15-gnb-results.xlsx'
    data_to_excel = pd.ExcelWriter(path)
    result_df.to_excel(data_to_excel)
    data_to_excel.book.save(path)

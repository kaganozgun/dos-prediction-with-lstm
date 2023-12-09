import pandas as pd
from sklearn.metrics import classification_report


def read_data(input_path, normal_attack_rate):
    data = pd.read_csv(input_path + "/data_w_selected_features.csv")
    data = data.dropna()
    data.loc[data["label"] == "BENIGN", "label_bn"] = 0
    data.loc[data["label"] != "BENIGN", "label_bn"] = 1
    df_normal = data.loc[data["label_bn"] == 0]
    df_dos = data.loc[data["label_bn"] == 1]
    dos_row_size = int(df_normal.shape[0] * (1 - normal_attack_rate) / normal_attack_rate)
    sampled_dos = df_dos.head(dos_row_size)
    sampled_df = pd.concat([sampled_dos, df_normal])
    sampled_df = sampled_df.sort_values(by=['timestamp'])
    sampled_df = sampled_df[['src_ip', 'ds_ip', 'label_bn']]
    print(sampled_df.info(verbose=True))
    return sampled_df


def calculate_rule_based_cicddos2019_srcip(data):
    result_df = pd.DataFrame()

    for window_1 in [20, 50, 100, 200]:
        for window_2_out in [300, 600, 1200, 1800, 2400, 3000]:
            x, y, y_pred_1, y_pred_2 = [], [], [], []
            for index in range(len(data)):
                out_index = index + window_1 + window_2_out - 1
                if out_index >= len(data):
                    break

                row = data.iloc[index]
                out_row = data.iloc[out_index]
                if row.src_ip != out_row.src_ip:
                    continue

                window = data.iloc[index: index + window_1]
                window_2 = data.iloc[index: index + window_1 + window_2_out]

                attack_cnt = window.loc[(window['src_ip'] == row.src_ip)]
                value_1 = 1 if len(attack_cnt) > 3 else 0
                value_2 = 1 if len(attack_cnt) > 5 else 0

                window_2 = window_2.values
                y.append(window_2[-1, -1])
                y_pred_1.append(value_1)
                y_pred_2.append(value_2)

            report_1 = classification_report(y, y_pred_1, output_dict=True)
            report_2 = classification_report(y, y_pred_2, output_dict=True)

            df_tmp = pd.DataFrame({'data_type': 'srcip',
                                   'rule': '>1',
                                   'win_1': window_1,
                                   'win_2': window_2_out,
                                   'pred_sec': window_2_out / 10,
                                   'accuracy': report_1["accuracy"],
                                   'recall_0': report_1["0.0"]["recall"],
                                   'recall_1': report_1["1.0"]["recall"],
                                   'precision_0': report_1["0.0"]["precision"],
                                   'precision_1': report_1["1.0"]["precision"],
                                   'f1_score_0': report_1["0.0"]["f1-score"],
                                   'f1_score_1': report_1["1.0"]["f1-score"],
                                   'accuracy_lvl_2': report_2["accuracy"],
                                   'recall_0_lvl_2': report_2["0.0"]["recall"],
                                   'recall_1_lvl_2': report_2["1.0"]["recall"],
                                   'precision_0_lvl_2': report_2["0.0"]["precision"],
                                   'precision_1_lvl_2': report_2["1.0"]["precision"],
                                   'f1_score_0_lvl_2': report_2["0.0"]["f1-score"],
                                   'f1_score_1_lvl_2': report_2["1.0"]["f1-score"]
                                   }, index=[0])
            result_df = pd.concat([result_df, df_tmp], ignore_index=True)

    path = 'results/cicddos2019-rule-based-srcip-results.xlsx'
    data_to_excel = pd.ExcelWriter(path)
    result_df.to_excel(data_to_excel)
    data_to_excel.book.save(path)


def calculate_rule_based_cicddos2019_dstip(data):
    result_df = pd.DataFrame()

    for window_1 in [20, 50, 100, 200]:
        for window_2_out in [300, 600, 1200, 1800, 2400, 3000]:
            x, y, y_pred_1, y_pred_2 = [], [], [], []
            for index in range(len(data)):
                out_index = index + window_1 + window_2_out - 1
                if out_index >= len(data):
                    break

                row = data.iloc[index]
                out_row = data.iloc[out_index]
                if row.ds_ip != out_row.ds_ip:
                    continue

                window = data.iloc[index: index + window_1]
                window_2 = data.iloc[index: index + window_1 + window_2_out]

                attack_cnt = window.loc[(window['ds_ip'] == row.ds_ip)]
                value_1 = 1 if len(attack_cnt) > 3 else 0
                value_2 = 1 if len(attack_cnt) > 5 else 0

                window_2 = window_2.values
                y.append(window_2[-1, -1])
                y_pred_1.append(value_1)
                y_pred_2.append(value_2)

            report_1 = classification_report(y, y_pred_1, output_dict=True)
            report_2 = classification_report(y, y_pred_2, output_dict=True)

            df_tmp = pd.DataFrame({'data_type': 'dstip',
                                   'rule': '>1',
                                   'win_1': window_1,
                                   'win_2': window_2_out,
                                   'pred_sec': window_2_out / 10,
                                   'accuracy': report_1["accuracy"],
                                   'recall_0': report_1["0.0"]["recall"],
                                   'recall_1': report_1["1.0"]["recall"],
                                   'precision_0': report_1["0.0"]["precision"],
                                   'precision_1': report_1["1.0"]["precision"],
                                   'f1_score_0': report_1["0.0"]["f1-score"],
                                   'f1_score_1': report_1["1.0"]["f1-score"],
                                   'accuracy_lvl_2': report_2["accuracy"],
                                   'recall_0_lvl_2': report_2["0.0"]["recall"],
                                   'recall_1_lvl_2': report_2["1.0"]["recall"],
                                   'precision_0_lvl_2': report_2["0.0"]["precision"],
                                   'precision_1_lvl_2': report_2["1.0"]["precision"],
                                   'f1_score_0_lvl_2': report_2["0.0"]["f1-score"],
                                   'f1_score_1_lvl_2': report_2["1.0"]["f1-score"]
                                   }, index=[0])
            result_df = pd.concat([result_df, df_tmp], ignore_index=True)

    path = 'results/cicddos2019-rule-based-dstip-results.xlsx'
    data_to_excel = pd.ExcelWriter(path)
    result_df.to_excel(data_to_excel)
    data_to_excel.book.save(path)


def calculate_rule_based_cicddos2019(input_path, sample_rate):
    data = read_data(input_path, sample_rate)
    calculate_rule_based_cicddos2019_srcip(data)
    calculate_rule_based_cicddos2019_dstip(data)

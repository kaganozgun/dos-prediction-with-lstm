import pandas as pd
from sklearn.metrics import classification_report


def read_data(input_path):
    col_names = ['srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl',
                 'sloss', 'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb',
                 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt',
                 'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd',
                 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm',
                 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attack_cat', 'Label']
    df_1 = pd.read_csv(f"{input_path}/UNSW-NB15_1.csv", names=col_names, header=None)
    df_2 = pd.read_csv(f"{input_path}/UNSW-NB15_2.csv", names=col_names, header=None)
    df_3 = pd.read_csv(f"{input_path}/UNSW-NB15_3.csv", names=col_names, header=None)
    df_4 = pd.read_csv(f"{input_path}/UNSW-NB15_4.csv", names=col_names, header=None)
    data = pd.concat([df_1, df_2, df_3, df_4], ignore_index=True)
    del df_1, df_2, df_3, df_4

    processed_data = data[['srcip', 'dstip', 'dsport', 'Label']]
    print(f'Raw input data shape: {processed_data.shape}')
    return processed_data


def calculate_rule_based_unswnb15_srcip_dport(data):
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
                if (row.srcip, row.dsport) != (out_row.srcip, out_row.dsport):
                    continue

                window = data.iloc[index: index + window_1]
                window_2 = data.iloc[index: index + window_1 + window_2_out]

                attack_cnt = window.loc[(window['srcip'] == row.dstip) & (window['dsport'] == row.dsport)]
                value_1 = 1 if len(attack_cnt) > 3 else 0
                value_2 = 1 if len(attack_cnt) > 5 else 0

                window_2 = window_2.values
                y.append(window_2[-1, -1])
                y_pred_1.append(value_1)
                y_pred_2.append(value_2)

            report_1 = classification_report(y, y_pred_1, output_dict=True)
            report_2 = classification_report(y, y_pred_2, output_dict=True)

            df_tmp = pd.DataFrame({'data_type': 'srcip-dport',
                                   'rule': '>1',
                                   'win_1': window_1,
                                   'win_2': window_2_out,
                                   'pred_sec': window_2_out / 10,
                                   'accuracy': report_1["accuracy"],
                                   'recall_0': report_1["0"]["recall"],
                                   'recall_1': report_1["1"]["recall"],
                                   'precision_0': report_1["0"]["precision"],
                                   'precision_1': report_1["1"]["precision"],
                                   'f1_score_0': report_1["0"]["f1-score"],
                                   'f1_score_1': report_1["1"]["f1-score"],
                                   'accuracy_lvl_2': report_2["accuracy"],
                                   'recall_0_lvl_2': report_2["0"]["recall"],
                                   'recall_1_lvl_2': report_2["1"]["recall"],
                                   'precision_0_lvl_2': report_2["0"]["precision"],
                                   'precision_1_lvl_2': report_2["1"]["precision"],
                                   'f1_score_0_lvl_2': report_2["0"]["f1-score"],
                                   'f1_score_1_lvl_2': report_2["1"]["f1-score"]
                                   }, index=[0])
            result_df = pd.concat([result_df, df_tmp], ignore_index=True)

    path = 'results/unswnb15-rule-based-srcip-dport-results.xlsx'
    data_to_excel = pd.ExcelWriter(path)
    result_df.to_excel(data_to_excel)
    data_to_excel.book.save(path)


def calculate_rule_based_unswnb15_dstip_dport(data):
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
                if (row.dstip, row.dsport) != (out_row.dstip, out_row.dsport):
                    continue

                window = data.iloc[index: index + window_1]
                window_2 = data.iloc[index: index + window_1 + window_2_out]

                attack_cnt = window.loc[(window['dstip'] == row.dstip) & (window['dsport'] == row.dsport)]
                value_1 = 1 if len(attack_cnt) > 3 else 0
                value_2 = 1 if len(attack_cnt) > 5 else 0

                window_2 = window_2.values
                y.append(window_2[-1, -1])
                y_pred_1.append(value_1)
                y_pred_2.append(value_2)

            report_1 = classification_report(y, y_pred_1, output_dict=True)
            report_2 = classification_report(y, y_pred_2, output_dict=True)

            df_tmp = pd.DataFrame({'data_type': 'dstip-dport',
                                   'rule': '>1',
                                   'win_1': window_1,
                                   'win_2': window_2_out,
                                   'pred_sec': window_2_out / 10,
                                   'accuracy': report_1["accuracy"],
                                   'recall_0': report_1["0"]["recall"],
                                   'recall_1': report_1["1"]["recall"],
                                   'precision_0': report_1["0"]["precision"],
                                   'precision_1': report_1["1"]["precision"],
                                   'f1_score_0': report_1["0"]["f1-score"],
                                   'f1_score_1': report_1["1"]["f1-score"],
                                   'accuracy_lvl_2': report_2["accuracy"],
                                   'recall_0_lvl_2': report_2["0"]["recall"],
                                   'recall_1_lvl_2': report_2["1"]["recall"],
                                   'precision_0_lvl_2': report_2["0"]["precision"],
                                   'precision_1_lvl_2': report_2["1"]["precision"],
                                   'f1_score_0_lvl_2': report_2["0"]["f1-score"],
                                   'f1_score_1_lvl_2': report_2["1"]["f1-score"]
                                   }, index=[0])
            result_df = pd.concat([result_df, df_tmp], ignore_index=True)

    path = 'results/unswnb15-rule-based-dstip-dport-results.xlsx'
    data_to_excel = pd.ExcelWriter(path)
    result_df.to_excel(data_to_excel)
    data_to_excel.book.save(path)


def calculate_rule_based_unswnb15(input_path):
    data = read_data(input_path)
    calculate_rule_based_unswnb15_srcip_dport(data)
    calculate_rule_based_unswnb15_dstip_dport(data)

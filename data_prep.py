#  Copyright (c) 2023. Kağan Özgün ITU Computer Engineering
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def read_data(base_path):
    col_names = ['srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl',
                 'sloss', 'dloss', 'service', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb',
                 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt',
                 'Dintpkt', 'tcprtt', 'synack', 'ackdat', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd',
                 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm',
                 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attack_cat', 'Label']
    df_1 = pd.read_csv(f"{base_path}/UNSW-NB15_1.csv", names=col_names, header=None)
    df_2 = pd.read_csv(f"{base_path}/UNSW-NB15_2.csv", names=col_names, header=None)
    df_3 = pd.read_csv(f"{base_path}/UNSW-NB15_3.csv", names=col_names, header=None)
    df_4 = pd.read_csv(f"{base_path}/UNSW-NB15_4.csv", names=col_names, header=None)
    data = pd.concat([df_1, df_2, df_3, df_4], ignore_index=True)
    del df_1, df_2, df_3, df_4
    # Explode categorical features
    service_categorical_cols = pd.get_dummies(data['service'], prefix='service', prefix_sep='_', dummy_na=False,
                                              columns=['service'], sparse=False, drop_first=False, dtype=None)
    state_categorical_cols = pd.get_dummies(data['state'], prefix='state', prefix_sep='_', dummy_na=False,
                                            columns=['state'], sparse=False, drop_first=False, dtype=None)
    proto_categorical_cols = pd.get_dummies(data['proto'], prefix='proto', prefix_sep='_', dummy_na=False,
                                            columns=['proto'], sparse=False, drop_first=False, dtype=None)
    data = data.drop(['service', 'state', 'proto'], axis=1)
    data = pd.concat([data, service_categorical_cols, state_categorical_cols, proto_categorical_cols], axis=1)
    del service_categorical_cols, state_categorical_cols, proto_categorical_cols
    data = data.sort_values(by=['Ltime'])
    print(f'Raw input data shape: {data.shape}')
    return data


def create_lstm_dataset(data, input_win_size, pred_win_size, output_type):
    x, y = [], []

    if output_type == 'srcip-dport':
        data = data.drop('dstip', axis=1)
        for index in range(len(data)):
            out_index = index + input_win_size + pred_win_size - 1
            if out_index >= len(data):
                break

            row = data.iloc[index]
            out_row = data.iloc[out_index]
            if (row.srcip, row.dsport) != (out_row.srcip, out_row.dsport):
                continue

            window = data.iloc[index: index + input_win_size].values
            window_2 = data.iloc[index: index + input_win_size + pred_win_size].values

            x.append(window[:, 2:-1])
            y.append(window_2[-1, -1])

    elif output_type == 'dstip-dport':
        data = data.drop('srcip', axis=1)
        for index in range(len(data)):
            out_index = index + input_win_size + pred_win_size - 1
            if out_index >= len(data):
                break

            row = data.iloc[index]
            out_row = data.iloc[out_index]
            if (row.dstip, row.dsport) != (out_row.dstip, out_row.dsport):
                continue

            window = data.iloc[index: index + input_win_size].values
            window_2 = data.iloc[index: index + input_win_size + pred_win_size].values

            x.append(window[:, 2:-1])
            y.append(window_2[-1, -1])
    else:
        print("Unknown type")

    x = np.dstack(x).astype("float32")
    y = np.dstack(y).astype("float32")
    x = x.transpose(2, 0, 1)
    y = y.transpose(2, 0, 1)
    return x, y


def prepare_train_val_test_split_and_save_to_file(x, y, test_rate, valid_rate, random_state, path):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_rate, random_state=random_state)
    if valid_rate != 0.0:
        x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=valid_rate/(1-test_rate), random_state=random_state)
        np.save(f"{path}/x_train_data.npy", x_train)
        np.save(f"{path}/x_test_data.npy", x_test)
        np.save(f"{path}/x_val_data.npy", x_valid)
        np.save(f"{path}/y_train_data.npy", y_train)
        np.save(f"{path}/y_test_data.npy", y_test)
        np.save(f"{path}/y_val_data.npy", y_valid)
    else:
        np.save(f"{path}/x_train_data.npy", x_train)
        np.save(f"{path}/x_test_data.npy", x_test)
        np.save(f"{path}/y_train_data.npy", y_train)
        np.save(f"{path}/y_test_data.npy", y_test)


def prepare_unsw_nb_15_all_dataset(base_path):
    input_path = f"{base_path}/Datasets/UNSW-NB15-CSV-Files"
    data = read_data(input_path)
    data = select_10_best_features(data)
    for t in ['srcip-dport', 'dstip-dport']: #, 'dstip-dport'
        print(f"Type: {t}")
        for w_1 in [20, 50, 100, 200]: # , 50, 100, 200
            for w_2 in [300, 600, 1200,1800, 2400, 3000]: # , 600, 1200,1800, 2400, 3000
                print(f"\t\twin_1: {w_1}, win_2: {w_2}")
                x, y = create_lstm_dataset(data, w_1, w_2, t)
                prepare_train_val_test_split_and_save_to_file(x, y, 0.2, 0.2, 42, f"{base_path}/lstm_prediction/data_prep/{t}/60-20-20/w{w_1}_p{w_2}")
                prepare_train_val_test_split_and_save_to_file(x, y, 0.2, 0.1, 42, f"{base_path}/lstm_prediction/data_prep/{t}/60-10-30/w{w_1}_p{w_2}")
                prepare_train_val_test_split_and_save_to_file(x, y, 0.3, 0.0, 42, f"{base_path}/lstm_prediction/data_prep/{t}/70-30/w{w_1}_p{w_2}")


def select_10_best_features(data):
    df = data[['srcip', 'dstip', 'dsport', 'state_INT', 'sttl', 'proto_wb-mon', 'service_-', 'service_dns',
               'ct_state_ttl','state_URN', 'ct_srv_dst', 'dmeansz', 'dttl', 'Label']]
    return df

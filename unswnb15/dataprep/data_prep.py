#  Copyright (c) 2023. Kağan Özgün ITU Computer Engineering
import pandas as pd
import numpy as np
from sklearn import preprocessing
import os
import gdown


def get_raw_data_from_gdrive(base_path):
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    url_1 = 'https://drive.google.com/uc?id=1Z52nd_a-vZsfMgu0X4ixV8S_S03yL8Al'
    output_1 = f"{base_path}/UNSW-NB15_1.csv"
    gdown.download(url_1, output_1, quiet=False)

    url_2 = 'https://drive.google.com/uc?id=12JoI35p41tQX8nHwHHwCXRyG9wDNNDJa'
    output_2 = f"{base_path}/UNSW-NB15_2.csv"
    gdown.download(url_2, output_2, quiet=False)

    url_3 = 'https://drive.google.com/uc?id=1r6UlCkDC05B3wntZCeEwQWyvnrZxdV_0'
    output_3 = f"{base_path}/UNSW-NB15_3.csv"
    gdown.download(url_3, output_3, quiet=False)

    url_4 = 'https://drive.google.com/uc?id=1BPjgzSDgnPz2TDRljz7kNtdkCwuTRESW'
    output_4 = f"{base_path}/UNSW-NB15_4.csv"
    gdown.download(url_4, output_4, quiet=False)


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
    data = data.drop(['service', 'state', 'proto', 'sport'], axis=1)
    data = pd.concat([data, service_categorical_cols, state_categorical_cols, proto_categorical_cols], axis=1)
    del service_categorical_cols, state_categorical_cols, proto_categorical_cols
    data = data.sort_values(by=['Ltime'])
    data = data.drop(['Ltime', 'Stime', 'attack_cat', 'ct_ftp_cmd'], axis=1)
    ip_ports_df = data[['srcip', 'dstip', 'dsport']]
    label_df = data[['Label']]
    without_ip_ports_df = data.drop(['srcip', 'dstip', 'dsport', 'Label'], axis=1)
    without_ip_ports_df_names = list(without_ip_ports_df.columns.values)
    x = without_ip_ports_df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    without_ip_ports_df = pd.DataFrame(x_scaled, columns=without_ip_ports_df_names)
    data = pd.concat([ip_ports_df, without_ip_ports_df, label_df], axis=1)
    data = data.fillna(0)
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
    x = x.transpose((2, 0, 1))
    y = y.transpose((2, 0, 1))
    return x, y


def prepare_train_val_test_split_and_save_to_file(x, y, test_rate, valid_rate, path):
    if not os.path.exists(path):
        os.makedirs(path)

    if valid_rate != 0.0:
        total_row_size = x.shape[0]
        train_row_size = int(total_row_size * (1 - test_rate - valid_rate))
        val_row_size = int(total_row_size * valid_rate)
        np.save(f"{path}/x_train_data.npy", x[:train_row_size, :, :])
        np.save(f"{path}/x_val_data.npy", x[train_row_size:(train_row_size + val_row_size), :, :])
        np.save(f"{path}/x_test_data.npy", x[(train_row_size + val_row_size):, :, :])
        np.save(f"{path}/y_train_data.npy", y[:train_row_size, :, :])
        np.save(f"{path}/y_val_data.npy", y[train_row_size:(train_row_size + val_row_size), :, :])
        np.save(f"{path}/y_test_data.npy", y[(train_row_size + val_row_size):, :, :])

    else:
        total_row_size = x.shape[0]
        train_row_size = int(total_row_size * (1 - test_rate))
        np.save(f"{path}/x_train_data.npy", x[:train_row_size, :, :])
        np.save(f"{path}/x_test_data.npy", x[train_row_size:, :, :])
        np.save(f"{path}/y_train_data.npy", y[:train_row_size, :, :])
        np.save(f"{path}/y_test_data.npy", y[train_row_size:, :, :])


def prepare_unsw_nb_15_all_dataset():
    base_path = "unswnb15/dataset"
    get_raw_data_from_gdrive(f"{base_path}/raw")
    data = read_data(f"{base_path}/raw")
    data = select_10_best_features(data)
    print(data.info(verbose=True))
    output_base_path = f"{base_path}/processed"

    for t in ['srcip-dport', 'dstip-dport']:
        print(f"Type: {t}")
        for w_1 in [20, 50, 100, 200]:
            for w_2 in [300, 600, 1200, 1800, 2400, 3000]:
                print(f"\t\twin_1: {w_1}, win_2: {w_2}")
                x, y = create_lstm_dataset(data, w_1, w_2, t)
                prepare_train_val_test_split_and_save_to_file(x, y, 0.2, 0.2, f"{output_base_path}/{t}/60-20-20/w{w_1}_p{w_2}")
                prepare_train_val_test_split_and_save_to_file(x, y, 0.2, 0.1, f"{output_base_path}/{t}/60-10-30/w{w_1}_p{w_2}")
                prepare_train_val_test_split_and_save_to_file(x, y, 0.3, 0.0, f"{output_base_path}/{t}/70-30/w{w_1}_p{w_2}")


def select_10_best_features(data):
    df = data[['srcip', 'dstip', 'dsport', 'state_INT', 'proto_wb-mon', 'service_-', 'service_dns', 'state_URN',
               'ct_srv_dst', 'dmeansz', 'sttl', 'dttl', 'ct_state_ttl', 'Label']]
    return df

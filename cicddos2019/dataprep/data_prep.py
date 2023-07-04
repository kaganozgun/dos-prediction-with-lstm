#  Copyright (c) 2023. Kağan Özgün ITU Computer Engineering
import pandas as pd
import numpy as np
from sklearn import preprocessing
import os
import gdown


def get_raw_data_from_gdrive(base_path):
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    url = 'https://drive.google.com/uc?id=15PcFtWWFTrzLqGuWqBic6aYkodkN2DUV'
    output = f"{base_path}/data_w_selected_features.csv"
    gdown.download(url, output, quiet=False)


def read_data(input_path, normal_attack_rate):
    data = pd.read_csv(input_path)
    data = data.dropna()
    data.loc[data["label"] == "BENIGN", "label_bn"] = 0
    data.loc[data["label"] != "BENIGN", "label_bn"] = 1
    df_normal = data.loc[data["label_bn"] == 0]
    df_dos = data.loc[data["label_bn"] == 1]
    dos_row_size = int(df_normal.shape[0] * (1-normal_attack_rate) / normal_attack_rate)
    sampled_dos = df_dos.head(dos_row_size)
    sampled_df = pd.concat([sampled_dos, df_normal])
    sampled_df = sampled_df.sort_values(by=['timestamp'])
    df_label = sampled_df['label_bn']
    sampled_df = sampled_df.drop(["label", "label_bn"], axis=1)
    df_concatted = pd.concat([sampled_df, df_label], axis=1)
    df_concatted = df_concatted.sort_values(by=['timestamp'])
    df_concatted = df_concatted.drop(["timestamp"], axis=1)

    ip_ports_df = df_concatted[['src_ip', 'ds_ip']]
    label_df = df_concatted[['label_bn']]
    ip_ports_df.reset_index(inplace=True)
    ip_ports_df = ip_ports_df.drop('index', axis=1)
    label_df.reset_index(inplace=True)
    without_ip_ports_df = df_concatted.drop(['src_ip', 'ds_ip', 'ds_port', 'label_bn'], axis=1)
    without_ip_ports_df_names = list(without_ip_ports_df.columns.values)
    for col_name in without_ip_ports_df_names:
        max_value = np.nanmax(without_ip_ports_df[col_name][without_ip_ports_df[col_name] != np.inf])
        min_value = np.nanmin(without_ip_ports_df[col_name][without_ip_ports_df[col_name] != -np.inf])
        without_ip_ports_df[col_name].replace([np.inf], max_value, inplace=True)
        without_ip_ports_df[col_name].replace([-np.inf], min_value, inplace=True)
    x = without_ip_ports_df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    without_ip_ports_df = pd.DataFrame(x_scaled, columns=without_ip_ports_df_names)
    data = pd.concat([ip_ports_df, without_ip_ports_df, label_df['label_bn']], axis=1)
    print(data.info(verbose=True))
    return data


def create_lstm_dataset(data, input_win_size, pred_win_size, output_type):
    x, y = [], []

    if output_type == 'srcip':
        data = data.drop('ds_ip', axis=1)
        for index in range(len(data)):
            out_index = index + input_win_size + pred_win_size - 1
            if out_index >= len(data):
                break

            row = data.iloc[index]
            out_row = data.iloc[out_index]
            if row.src_ip != out_row.src_ip:
                continue

            window = data.iloc[index: index + input_win_size].values
            window_2 = data.iloc[index: index + input_win_size + pred_win_size].values

            x.append(window[:, 1:-1])
            y.append(window_2[-1, -1])

    elif output_type == 'dstip':
        data = data.drop('src_ip', axis=1)
        for index in range(len(data)):
            out_index = index + input_win_size + pred_win_size - 1
            if out_index >= len(data):
                break

            row = data.iloc[index]
            out_row = data.iloc[out_index]
            if row.ds_ip != out_row.ds_ip:
                continue

            window = data.iloc[index: index + input_win_size].values
            window_2 = data.iloc[index: index + input_win_size + pred_win_size].values

            x.append(window[:, 1:-1])
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


def prepare_cicddos2019_all_dataset():
    base_path = "cicddos2019/dataset"
    get_raw_data_from_gdrive(f"{base_path}/raw")
    input_path = f"{base_path}/raw/data_w_selected_features.csv"
    data = read_data(input_path, 0.3)
    output_base_path = f"{base_path}/processed"

    for t in ['dstip', 'srcip']:
        print(f"Type: {t}")
        for w_1 in [20, 50, 100, 200]:
            for w_2 in [300, 600, 1200, 1800, 2400, 3000]:
                print(f"\t\twin_1: {w_1}, win_2: {w_2}")
                x, y = create_lstm_dataset(data, w_1, w_2, t)
                prepare_train_val_test_split_and_save_to_file(x, y, 0.2, 0.2, f"{output_base_path}/{t}/60-20-20/w{w_1}_p{w_2}")
                prepare_train_val_test_split_and_save_to_file(x, y, 0.2, 0.1, f"{output_base_path}/{t}/60-10-30/w{w_1}_p{w_2}")
                prepare_train_val_test_split_and_save_to_file(x, y, 0.3, 0.0, f"{output_base_path}/{t}/70-30/w{w_1}_p{w_2}")

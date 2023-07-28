import tensorflow as tf
import numpy as np


def create_lstm_model():
    model = tf.keras.Sequential(
        [
            tf.keras.layers.LSTM(32, return_sequences=True),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(16, return_sequences=False),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    return model


def cicddos2019_train_lstm_model(base_path):
    for split_shape in ["60-20-20", "60-10-30", "70-30"]:
        print(f"Split shape: {split_shape}")
        for window_1 in [20, 50, 100, 200]:
            print(f"\tWindow 1: {window_1}")
            for window_2 in [300, 600, 1200, 1800, 2400, 3000]:
                print(f"\t\tWindow 2: {window_2}")
                for t in ["dstip", "srcip"]:
                    print(f"\t\t\tType: {t}")
                    path = base_path + "/" + t + "/" + split_shape + "/w" + str(window_1) + "_p" + str(window_2)
                    x_train = np.load(f"{path}/x_train_data.npy")
                    y_train = np.load(f"{path}/y_train_data.npy")

                    model = create_lstm_model()
                    y_train = y_train.reshape(-1)

                    if split_shape != "70-30":
                        x_valid = np.load(f"{path}/x_val_data.npy")
                        y_valid = np.load(f"{path}/y_val_data.npy")
                        y_valid = y_valid.reshape(-1)

                        early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, mode="min")

                        model.fit(
                            x_train,
                            y_train,
                            epochs=50,
                            validation_data=(x_valid, y_valid),
                            callbacks=[early_stopping]
                        )

                    else:
                        early_stopping = tf.keras.callbacks.EarlyStopping(monitor="loss", patience=5, mode="min")

                        model.fit(
                            x_train,
                            y_train,
                            epochs=50,
                            callbacks=[early_stopping],
                        )

                    model.save(f"{path}/final.h5")

# dos-prediction-with-lstm

reproduce experiments result with following commands

#### Download raw dataset from Google Drive and run data preparation methods
 - python main.py  -d unswnb15 -m data-prep
 - python main.py  -d cicddos2019 -m data-prep

#### Run rule-based method
 - python main.py  -d unswnb15 -m rule-based
 - python main.py  -d cicddos2019 -m rule-based

#### Run Gaussian Naive Bayes method
 - python main.py  -d unswnb15 -m gnb
 - python main.py  -d cicddos2019 -m gnb

#### Run Long Short-Term Memory method
 - python main.py  -d unswnb15 -m lstm
 - python main.py  -d cicddos2019 -m lstm

results of the experiments produced as xlsx file under "/results" folder
Processed data and models are collect under "/unswnb15/dataset/processed" and "/cicddos2019/dataset/processed" folder

### Best 10 features of UNSW-NB15 dataset selected for models given below:

| Feature      | Explanation                                                                                                                                |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| ct\_srv\_dst  | No. of connections that contain the same service and destination address in 100 connections according to the last time.                    |
| ct\_state\_ttl | No. for each state according to specific range of values for source/destination time to live.                                              |
| sttl            | Source to destination time to live value.                                                                                                  |
| dttl             | Destination to source time to live value.                                                                                                  |
| dmeansz           | Mean of the packet size transmitted by the destination                                                                                     |
| state\_INT         | Indicates to the state and its dependent protocol, e.g. ACC, CLO, CON, ECO, ECR, FIN, INT, MAS, PAR, REQ, RST, TST, TXD, URH, URN, and (-) |
| state\_URN          | same categories as above                                                                                                                   |
| service\_dns         | http, ftp, smtp, ssh, dns, ftp-data ,irc  and (-)                                                                                          |
| service\_-            | same categories as above                                                                                                                   |
| proto\_wb\_mon        | Used protocol WIDEBAND Monitoring                                                                                                          |

### Best 10 features of CIC-DDoS2019 dataset selected for models given below:

| Feature               | Explanation                                                                                                                      |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------|
| bwd\_packet\_len\_std | Standart deviation of backward packet length.                                                                                    |
| bwd\_header\_len     | Backward header length.                                                                                                          |
| bwd\_iat\_total     | Total of backward packet inter-arrival time.                                                                                     |
| fwd\_iat\_mean     | Mean of forward packet inter-arrival time.                                                                                       |
| fwd\_iat\_total   | Total of forward packet inter-arrival time.                                                                                      |
| fwd\_iat\_std    | Standart deviation of forward packet inter-arrival time.                                                                                   |
| flow\_iat\_std   | Standart deviation of data flow inter-arrival time.                                                                                        |
| flow\_iat\_mean | Mean of data flow inter-arrival time.                                                                                                      |
| active\_std   | Standart deviation of active time on network.                                                                                              |
| dur\_total   | Total duration of packet                                                                                                                   |

### Extended result table

| Model | Dataset | Group By | Alert Level | Config | Accuracy | Recall | Precision | F1 Score |
|-------|-|-|-|---------------|-|---------------|---------------|---------------|
|   Rule-based model    | UNSW-NB15    | dstip-dport | Level 1     | 100 / 60               | 0.56     | 0.15 / 0.97            | 0.85 / 0.53               | 0.25 / 0.69              |
|    Rule-based model   | UNSW-NB15 | dstip-dport | Level 2 | 100 / 60      | 0.58 | 0.19 / 0.95   | 0.81 / 0.54   | 0.31 / 0.64   |
|   Rule-based model    | UNSW-NB15 | srcip-dport | Level 1 | 100 / 60      | 0.50 | 0.28 / 0.72   | 0.50 / 0.50   | 0.36 / 0.59   |
|   Rule-based model    | UNSW-NB15 | srcip-dport | Level 2 | 100 / 60      | 0.50 | 0.29 / 0.71   | 0.50 / 0.50   | 0.24 / 0.60   |
|   Rule-based model    | UNSW-NB15 | dstip-dport | Level 1 | 200 / 180     | 0.54 | 0.09 / 0.99   | 0.96 / 0.52   | 0.16 / 0.68   |
|   Rule-based model    | UNSW-NB15 | dstip-dport | Level 2 | 200 / 180     | 0.56 | 0.14 / 0.99   | 0.96 / 0.53   | 0.24 / 0.69   |
|   Rule-based model    | UNSW-NB15 | srcip-dport | Level 1 | 200 / 180     | 0.49 | 0.20 / 0.78   | 0.48 / 0.49   | 0.28 / 0.60   |
|   Rule-based model    | UNSW-NB15 | srcip-dport | Level 2 | 200 / 180     | 0.49 | 0.20 / 0.78   | 0.48 / 0.49   | 0.28 / 0.60   |
|   Rule-based model    | UNSW-NB15 | dstip-dport | Level 1 | 200 / 300     | 0.53 | 0.09 / 0.99   | 0.95 / 0.51   | 0.16 / 0.67   |
|    Rule-based model   | UNSW-NB15 | dstip-dport | Level 2 | 200 / 300     | 0.55 | 0.14 / 0.99   | 0.95 / 0.52   | 0.24 / 0.68   |
|   Rule-based model    | UNSW-NB15 | srcip-dport | Level 1 | 200 / 300     | 0.49 | 0.19 / 0.80   | 0.51 / 0.49   | 0.28 / 0.61   |
|   Rule-based model    | UNSW-NB15 | srcip-dport | Level 2 | 200 / 300     | 0.49 | 0.19 / 0.80   | 0.51 / 0.49   | 0.28 / 0.61   |
|   Rule-based model    | CIC-DDoS2019 | dstip | Level 1 | 100 / 60      | 0.95 | 0.08 / 0.99   | 0.98 / 0.95   | 0.08 / 0.98   |
|   Rule-based model    | CIC-DDoS2019 | dstip | Level 2 | 100 / 60      | 0.96 | 0.08 / 0.99   | 0.95 / 0.96   | 0.14 / 0.98   |
|   Rule-based model    | CIC-DDoS2019 | srcip | Level 1 | 100 / 60      | 0.91 | 0.03 / 0.99   | 0.99 / 0.91   | 0.06 / 0.96   |
|   Rule-based model    | CIC-DDoS2019 | srcip | Level 2 | 100 / 60      | 0.92 | 0.05 / 0.99   | 0.96 / 0.92   | 0.10 / 0.96   |
|   Rule-based model    | CIC-DDoS2019 | dstip | Level 1 | 200 / 180     | 0.96 | 0.02 / 0.99   | 0.94 / 0.96   | 0.03 / 0.98   |
|   Rule-based model    | CIC-DDoS2019 | dstip | Level 2 | 200 / 180     | 0.96 | 0.03 / 0.99   | 0.94 / 0.96   | 0.06 / 0.98   |
|   Rule-based model    | CIC-DDoS2019 | srcip | Level 1 | 200 / 180     | 0.92 | 0.01 / 0.99   | 0.99 / 0.92   | 0.02 / 0.96   |
|   Rule-based model    | CIC-DDoS2019 | srcip | Level 2 | 200 / 180     | 0.92 | 0.02 / 0.99   | 0.98 / 0.92   | 0.04 / 0.96   |
|   Rule-based model    | CIC-DDoS2019 | dstip | Level 1 | 200 / 300     | 0.96 | 0.02 / 0.99   | 0.93 / 0.96   | 0.03 / 0.99   |
|   Rule-based model    | CIC-DDoS2019 | dstip | Level 2 | 200 / 300     | 0.96 | 0.03 / 0.99   | 0.93 / 0.96   | 0.06 / 0.98   |
|   Rule-based model    | CIC-DDoS2019 | srcip | Level 1 | 200 / 300     | 0.93 | 0.01 / 0.99   | 0.99 / 0.93   | 0.02 / 0.99   |
|   Rule-based model    | CIC-DDoS2019 | srcip | Level 2 | 200 / 300     | 0.93 | 0.02 / 0.99   | 0.99 / 0.93   | 0.03 / 0.96   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | dstip-dport | Level 1 | 100 / 60      | 0.54 | 0.99 / 0.01   | 0.54 / 0.97   | 0.70 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | dstip-dport | Level 2 | 100 / 60      | 0.54 | 0.99 / 0.01   | 0.54 / 0.97   | 0.70 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | dstip-dport | Level 1 | 200 / 180     | 0.56 | 0.99 / 0.01   | 0.56 / 0.98   | 0.72 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | dstip-dport | Level 2 | 200 / 180     | 0.56 | 0.99 / 0.01   | 0.56 / 0.98   | 0.72 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | dstip-dport | Level 1 | 200 / 300     | 0.56 | 0.99 / 0.01   | 0.56 / 0.94   | 0.72 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | dstip-dport | Level 2 | 200 / 300     | 0.56 | 0.99 / 0.01   | 0.56 / 0.94   | 0.72 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | srcip-dport | Level 1 | 100 / 60      | 0.54 | 0.99 / 0.01   | 0.54 / 0.97   | 0.70 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | srcip-dport | Level 2 | 100 / 60      | 0.54 | 0.99 / 0.01   | 0.54 / 0.97   | 0.70 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | srcip-dport | Level 1 | 200 / 180     | 0.56 | 0.99 / 0.01   | 0.56 / 0.98   | 0.72 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | srcip-dport | Level 2 | 200 / 180     | 0.56 | 0.99 / 0.01   | 0.56 / 0.98   | 0.72 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | srcip-dport | Level 1 | 200 / 300     | 0.56 | 0.99 / 0.01   | 0.56 / 0.95   | 0.72 / 0.01   |
|   Gaussian Naive Bayes model    | UNSW-NB15 | srcip-dport | Level 2 | 200 / 300     | 0.56 | 0.99 / 0.01   | 0.56 / 0.95   | 0.72 / 0.01   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | dstip | Level 1 | 100 / 60      | 0.98 | 0.80 / 0.99   | 0.99 / 0.97   | 0.89 / 0.99   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | dstip | Level 2 | 100 / 60      | 0.98 | 0.80 / 0.99   | 0.99 / 0.97   | 0.89 / 0.99   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | dstip | Level 1 | 200 / 180     | 0.98 | 0.82 / 0.99   | 0.99 / 0.98   | 0.90 / 0.99   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | dstip | Level 2 | 200 / 180     | 0.98 | 0.80 / 0.99   | 0.99 / 0.98   | 0.90 / 0.99   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | dstip | Level 1 | 200 / 300     | 0.98 | 0.77 / 0.99   | 0.99 / 0.97   | 0.87 / 0.99   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | dstip | Level 2 | 200 / 300     | 0.98 | 0.77 / 0.99   | 0.99 / 0.97   | 0.87 / 0.99   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | srcip | Level 1 | 100 / 60      | 0.94 | 0.71 / 0.99   | 0.99 / 0.93   | 0.83 / 0.96   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | srcip | Level 2 | 100 / 60      | 0.94 | 0.71 / 0.99   | 0.99 / 0.93   | 0.83 / 0.96   |
|  Gaussian Naive Bayes model     | CIC-DDoS2019 | srcip | Level 1 | 200 / 180     | 0.94 | 0.72 / 0.99   | 0.99 / 0.93   | 0.84 / 0.96   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | srcip | Level 2 | 200 / 180     | 0.94 | 0.72 / 0.99   | 0.99 / 0.93   | 0.84 / 0.96   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | srcip | Level 1 | 200 / 300     | 0.94 | 0.68 / 0.99   | 0.99 / 0.93   | 0.81 / 0.96   |
|   Gaussian Naive Bayes model    | CIC-DDoS2019 | srcip | Level 2 | 200 / 300     | 0.94 | 0.68 / 0.99   | 0.99 / 0.93   | 0.81 / 0.96   |
|   LSTM model    | UNSW-NB15 | dstip-dport | Level 1 | 100 / 60      | 0.82 | 0.84 / 0.80   | 0.83 / 0.81   | 0.84 / 0.81   |
|   LSTM model    | UNSW-NB15 | dstip-dport | Level 2 | 100 / 60      | 0.82 | 0.92 / 0.71   | 0.79 / 0.88   | 0.85 / 0.78   |
|   LSTM model    | UNSW-NB15 | dstip-dport | Level 1 | 200 / 180     | 0.83 | 0.82 / 0.83   | 0.86 / 0.79   | 0.84 / 0.81   |
|   LSTM model    | UNSW-NB15 | dstip-dport | Level 2 | 200 / 180     | 0.82 | 0.91 / 0.70   | 0.79 / 0.87   | 0.85 / 0.78   |
|   LSTM model    | UNSW-NB15 | dstip-dport | Level 1 | 200 / 300     | 0.82 | 0.79 / 0.85   | 0.87 / 0.76   | 0.83 / 0.80   |
|   LSTM model    | UNSW-NB15 | dstip-dport | Level 2 | 200 / 300     | 0.83 | 0.89 / 0.75   | 0.82 / 0.85   | 0.85 / 0.79   |
|   LSTM model    | UNSW-NB15 | srcip-dport | Level 1 | 100 / 60      | 0.82 | 0.84 / 0.80   | 0.83 / 0.81   | 0.84 / 0.81   |
|   LSTM model    | UNSW-NB15 | srcip-dport | Level 2 | 100 / 60      | 0.81 | 0.91 / 0.70   | 0.78 / 0.87   | 0.84 / 0.78   |
|   LSTM model    | UNSW-NB15 | srcip-dport | Level 1 | 200 / 180     | 0.82 | 0.81 / 0.84   | 0.86 / 0.78   | 0.83 / 0.81   |
|   LSTM model    | UNSW-NB15 | srcip-dport | Level 2 | 200 / 180     | 0.82 | 0.89 / 0.74   | 0.81 / 0.85   | 0.85 / 0.79   |
|   LSTM model    | UNSW-NB15 | srcip-dport | Level 1 | 200 / 300     | 0.83 | 0.83 / 0.82   | 0.85 / 0.79   | 0.84 / 0.81   |
|   LSTM model    | UNSW-NB15 | srcip-dport | Level 2 | 200 / 300     | 0.83 | 0.90 / 0.74   | 0.81 / 0.85   | 0.85 / 0.79   |
|   LSTM model    | CIC-DDoS2019 | dstip | Level 1 | 100 / 60      | 0.99 | 0.92 / 0.99   | 0.99 / 0.99   | 0.96 / 0.99   |
|   LSTM model    | CIC-DDoS2019 | dstip | Level 2 | 100 / 60      | 0.99 | 0.93 / 0.99   | 0.99 / 0.99   | 0.96 / 0.99   |
|   LSTM model    | CIC-DDoS2019 | dstip | Level 1 | 200 / 180     | 0.99 | 0.95 / 0.99   | 0.99 / 0.99   | 0.97 / 0.99   |
|   LSTM model    | CIC-DDoS2019 | dstip | Level 2 | 200 / 180     | 0.99 | 0.96 / 0.99   | 0.99 / 0.99   | 0.98 / 0.99   |
|   LSTM model    | CIC-DDoS2019 | dstip | Level 1 | 200 / 300     | 0.96 | 0.61 / 0.99   | 0.99 / 0.96   | 0.76 / 0.99   |
|   LSTM model    | CIC-DDoS2019 | dstip | Level 2 | 200 / 300     | 0.97 | 0.70 / 0.99   | 0.99 / 0.97   | 0.82 / 0.99   |
|  LSTM model     | CIC-DDoS2019 | srcip | Level 1 | 100 / 60      | 0.98 | 0.90 / 0.99   | 0.99 / 0.97   | 0.95 / 0.99   |
|   LSTM model    | CIC-DDoS2019 | srcip | Level 2 | 100 / 60      | 0.98 | 0.91 / 0.99   | 0.99 / 0.97   | 0.95 / 0.99   |
|   LSTM model    | CIC-DDoS2019 | srcip | Level 1 | 200 / 180     | 0.97 | 0.85 / 0.99   | 0.99 / 0.96   | 0.92 / 0.98   |
|   LSTM model    | CIC-DDoS2019 | srcip | Level 2 | 200 / 180     | 0.97 | 0.85 / 0.99   | 0.99 / 0.96   | 0.92 / 0.98   |
|   LSTM model    | CIC-DDoS2019 | srcip | Level 1 | 200 / 300     | 0.96 | 0.77 / 0.99   | 0.99 / 0.95   | 0.87 / 0.97   |
|   LSTM model    | CIC-DDoS2019 | srcip | Level 2 | 200 / 300     | 0.96 | 0.79 / 0.99   | 0.99 / 0.95   | 0.88 / 0.98   |

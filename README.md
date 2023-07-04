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


# Video Moment Retrieval in Practical Setting: A Dataset of Ranked Moments for  Imprecise  Queries

The benchmark and dataset for the paper "Video Moment Retrieval in Practical Setting: A Dataset of Ranked Moments for  Imprecise  Queries", comming soon...


![vmr_ranking_overview](./figures/taskComparisonV.jpg)

> The codes are modified from [ReLoCLNet](https://github.com/26hzhang/ReLoCLNet).



## Getting started
### 1. Install the requisites

The Python packages we used were listed as follows.
Commonly, the most recent versions work well.


```shell
conda create --name tvr_ranking python=3.11
conda activate tvr_ranking
pip install pytorch # 2.2.1+cu121
pip install tensorboard 
pip install h5py pandas tqdm easydict pyyaml
```
The conda environment of [ReLoCLNet](https://github.com/26hzhang/ReLoCLNet) also works.

### 2. Download full dataset
For the full dataset, please go down from [TVR-Ranking](
https://drive.google.com/drive/folders/1QuE3Ah1VR_Sudjbl_5VFC1J-aT9Dh_WF?usp=drive_link) and organized as follows
```
TVR_Ranking/
  -val.json                  
  -test.json                 
  -train_top01.jsonl
  -train_top20.json
  -train_top40.jsonl
  -video_name_duration_id.json
```
The detailed introduction and raw annotations is available at [TVR_Ranking Introduction](data/TVR_Ranking/readme.md).

### 3. Download features

For the features of the TVR dataset, you can request them from [TVR](https://tvr.cs.unc.edu/) or download them from [TVR features on Hugging Face](https://huggingface.co/datasets/k-nick/NLVL).

```shell
tar -xf tvr_feature_release.tar.gz -C data
```

### 4. Training
```shell
# modify the data path first 
sh run_top01.sh
```

## Baseline
The baseline performance of  $NDGC@20$ was shown as follows.
Top $N$ moments were comprised of a pseudo training set by the query-caption similarity.
| Model          | $N$ | IoU = 0.3, val | IoU = 0.3, test | IoU = 0.5, val | IoU = 0.5, test | IoU = 0.7, val | IoU = 0.7, test |
|----------------|-----|----------------|-----------------|----------------|-----------------|----------------|-----------------|
| **XML**        | 1   | 0.1050         | 0.1047          | 0.0767         | 0.0751          | 0.0287         | 0.0314          |
|                | 20  | 0.1948         | 0.1964          | 0.1417         | 0.1434          | 0.0519         | 0.0583          |
|                | 40  | 0.2101         | 0.2110          | 0.1525         | 0.1533          | 0.0613         | 0.0617          |
| **CONQUER**    | 1   | 0.0979         | 0.0830          | 0.0817         | 0.0686          | 0.0547         | 0.0479          |
|                | 20  | 0.2007         | 0.1935          | 0.1844         | 0.1803          | 0.1391         | 0.1341          |
|                | 40  | 0.2094         | 0.1943          | 0.1930         | 0.1825          | 0.1481         | 0.1334          |
| **ReLoCLNet**  | 1   | 0.1306         | 0.1299          | 0.1169         | 0.1154          | 0.0738         | 0.0789          |
|                | 20  | 0.3264         | 0.3214          | 0.3007         | 0.2956          | 0.2074         | 0.2084          |
|                | 40  | 0.3479         | 0.3473          | 0.3221         | 0.3217          | 0.2218         | 0.2275          |



The checkpoint can all be accessed from [CheckPoints](https://drive.google.com/drive/folders/1hXJn-5ORA8T1Iyx6K2BK7KnUOpCQD9Na?usp=drive_link).


## Citation
If you feel this project helpful to your research, please cite our work.
```

```

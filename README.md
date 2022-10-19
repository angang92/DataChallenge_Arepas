# DataChallenge_Arepas

The goal is to prepare the training dataset for a model that will help kitchen workers to know when to stop a machine for maintenance actions.

## 2A_hourlyAveragedMetrics.py

Users have at their disposal the following datasets, in /data folder:
- cooking_metrics: a table containing two metrics (metric_1, metric_2) retrieved by each machine at a specific timestamp ad associated to phase 1 of a specific batch
- batch_registry: a table cotaining the correspondance between batch and arepa type
- faulty_intervals: a table containinf for each machine the intervals in which metrics data are not reliable

The program is expected to receive:
- machine id (e.g. m1)
- arepa type id (e.g. a1)
- start time (YYYYMM-DDTHH:MM:SS)
- end time (YYYYMM-DDTHH:MM:SS)

The program produces a dataset with the hourly averaged metrics for a selected machine associated to a specified arepa type in the specified time interval.
Faulty data are labeled as "non reliable", according to faulty_intervals dataset, and filtered out before calculating mean value.

Program output is a csv file "training_data.csv".

### How to use 2A_hourlyAveragedMetrics.py

python -W ignore 2A_hourlyAveragedMetrics.py <machine_id> <arepa_type> <start_time> <end_time>

e.g. python -W ignore 2A_hourlyAveragedMetrics.py m1 a1 2020-11-01T01:00:00 2020-11-01T02:00:00


## 2B_hourlyAveragedMetrics_ArepaList.py

Users have at their disposal the following datasets, in /data folder:
- cooking_metrics: a table containing two metrics (metric_1, metric_2) retrieved by each machine at a specific timestamp ad associated to phase 1 of a specific batch
- batch_registry: a table cotaining the correspondance between batch and arepa type
- faulty_intervals: a table containinf for each machine the intervals in which metrics data are not reliable
- arepa_list: a txt cointaining a list of arepa type code


The program is expected to receive:
- arepa type list file path (e.g. data/arepa_list.txt)
- start time (YYYYMM-DDTHH:MM:SS)
- end time (YYYYMM-DDTHH:MM:SS)

The program produces a dataset with the hourly averaged metrics for all machines associated to a list of specified arepa type in the specified time interval.
Faulty data are labeled as "non reliable", according to faulty_intervals dataset, and filtered out before calculating mean value.

Program output is a csv file "training_data2.csv".

### How to use 2B_hourlyAveragedMetrics_ArepaList.py

python -W ignore 2B_hourlyAveragedMetrics_ArepaList.py <arepa_list> <start_time> <end_time>

e.g. python -W ignore 2A_hourlyAveragedMetrics.py data/arepa_list.txt 2020-11-01T01:00:00 2020-11-01T02:00:00

import pandas as pd
import numpy as np
import argparse 
import os
# Determine if dt is between dt1 and dt2 (True/False)
class DatetimeRange:
    def __init__(self, dt1, dt2):
        self._dt1 = dt1
        self._dt2 = dt2

    def __contains__(self, dt):
        return self._dt1 < dt < self._dt2
        
              
def countX(lst, x):
    """
    Count occurrence of x in list lst
    
    :param lst: list object
    :param x: element to find
    :return: occurrence of x in lst
    """
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count
    
def main():
    print("============================================")
    print("Generate hourly averaged metrics for a specified machine and arepa type")
    print("============================================")



    parser = argparse.ArgumentParser(description="Genera metriche orarie per specifica macchina e tipologia di arepa")

    parser.add_argument('machine', metavar='MACHINE', type=str,
                        help='ID macchina')
    parser.add_argument('arepa', metavar='AREPA', type=str,
                        help='ID arepa type')
    parser.add_argument('start_time', metavar='STARTTIME', type=str,
                        help='start time: YYYYMM-DDTHH:MM:SS')
    parser.add_argument('end_time', metavar='ENDTIME', type=str,
                        help='end time: YYYYMM-DDTHH:MM:SS')

    args = parser.parse_args()

    # Import csv datasets
    metrics = pd.read_csv('data/cooking_metrics.csv', sep=';')
    metrics

    batch = pd.read_csv('data/batch_registry.csv', sep=';')
    batch

    fault = pd.read_csv('data/faulty_intervals.csv', sep=';')
    fault

    df = pd.merge(metrics, batch, on='batch_id', how='left')
    df

    machine = args.machine
    arepa = args.arepa
    start_time = args.start_time
    end_time = args.end_time

    # Filter data
    df_m1 = df[(df.machine_id == machine) & (df.arepa_type == arepa)] # metrics for selected machine ad arepa type

    fault_m1 = fault[fault.machine_id == machine] # fault intervals for selected machine
                  
    df_m1['reliable'] = '' # add column to dataframe 

    # for every row in metrics dataframe, finds if the timestamp is between every faulty interval
    for ind in df_m1.index:
        not_reliable = []
        for f_int in fault_m1.index:
            not_reliable.append(df_m1['timestamp'][ind] in DatetimeRange(fault_m1['start_time'][f_int], fault_m1['end_time'][f_int])) 
        
        df_m1['reliable'][ind] = np.where(countX(not_reliable, True) > 0, 'NO','YES') # specifies if the metric is collected in a faulty interval: reliable = 'NO'

    df_m1

    # convert metrics to float datatype
    df_m1['metric_1'] = df_m1['metric_1'].replace(',','.', regex=True).astype(float)
    df_m1['metric_2'] = df_m1['metric_2'].replace(',','.', regex=True).astype(float)

    # filter only data in specified data range and realiable
    filtered_df = df_m1[(df_m1['timestamp'] >= start_time) & (df_m1['timestamp'] <= end_time) & (df_m1['reliable'] == 'YES')]
    val1 = filtered_df['metric_1'].mean()
    val2 = filtered_df['metric_2'].mean()


    # write results to csv file
    import csv

    header = ['start_time', 'end_time', 'machine_id', 'arepa_type', 'avg_metric_1', 'avg_metric_2']
    data = [start_time, end_time, machine, arepa, val1, val2]

    filename = 'data/training_data.csv'
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', encoding = 'UTF8', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        
        writer.writerow(data)
        
        
        
if __name__ == "__main__":
    main()


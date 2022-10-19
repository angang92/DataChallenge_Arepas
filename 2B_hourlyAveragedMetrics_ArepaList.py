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
    print("====================================================================================")
    print("Generate hourly averaged metrics for a list of specified arepas and all machines")
    print("====================================================================================")



    parser = argparse.ArgumentParser(description="Genera metriche orarie per tutte le macchine e per una lista di tipologie di arepa")

    parser.add_argument('arepa_list', metavar='AREPALIST', type=str,
                        help='Arepa list file (txt)')
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

    # arepa_list = 'data/arepa_list.txt'
    # start_time = '2020-11-01T01:00:00'
    # end_time = '2020-11-01T02:00:00'
    
    arepa_list = args.arepa_list
    start_time = args.start_time
    end_time = args.end_time
    
    f = open(arepa_list,'r')
    text_list = f.readlines()
    arepas = []
    for i in range(len(text_list)):
        arepas.extend(text_list[i].rstrip('\n').split(','))

    # Filter data
    df_m1 = df[df['arepa_type'].isin(arepas)] # metrics for selected arepa types
                 
    df_m1['reliable'] = '' # add column to dataframe 

    # for every row in metrics dataframe, finds if the timestamp is between every faulty interval
    for ind in df_m1.index:
        not_reliable = []
        for f_int in fault.index:
            not_reliable.append(df_m1['timestamp'][ind] in DatetimeRange(fault['start_time'][f_int], fault['end_time'][f_int])) 
        
        df_m1['reliable'][ind] = np.where(countX(not_reliable, True) > 0, 'NO','YES') # specifies if the metric is collected in a faulty interval: reliable = 'NO'

    df_m1

    # convert metrics to float datatype
    df_m1['metric_1'] = df_m1['metric_1'].replace(',','.', regex=True).astype(float)
    df_m1['metric_2'] = df_m1['metric_2'].replace(',','.', regex=True).astype(float)
    
    # get unique list of machines
    machines = df_m1['machine_id'].unique()


    # filter only data in specified data range and realiable
    import csv

    for m in machines:
        filtered_df = df_m1[(df_m1['machine_id'] == m) & (df_m1['timestamp'] >= start_time) & (df_m1['timestamp'] <= end_time) & (df_m1['reliable'] == 'YES')]
        val1 = filtered_df['metric_1'].mean()
        val2 = filtered_df['metric_2'].mean()

        header = ['start_time', 'end_time', 'machine_id', 'avg_metric_1', 'avg_metric_2']
        data = [start_time, end_time, m, val1, val2]

        filename = 'data/training_data_2.csv'
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', encoding = 'UTF8', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            
            writer.writerow(data)
        
        
if __name__ == "__main__":
    main()


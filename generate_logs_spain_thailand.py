# this script creates an event log from the raw data obtained from https://zenodo.org/records/14189193


import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.filtering import filter_case_size
from pm4py.objects.log.obj import EventLog, Trace
import pm4py


def preprocess_df(df):

    # remove events that arent reposts
    df = df[df['is_repost'] == True]  

    # remove unneccessary columns
    keep_columns = ['post_time', 'accountid', 'reposted_postid', 'is_control']
    df = df[keep_columns]

    # convert time to datetime
    df['post_time'] = pd.to_datetime(df['post_time'], unit='ms')

    # remove problematic ID characters
    df['accountid'] = df['accountid'].astype('str')
    df['accountid'] = df['accountid'].str.replace('[+=]', '', regex=True)
    df['accountid'] = ['u' + id for id in df['accountid']]

    # convert tweet ID to str
    df['reposted_postid'] = df['reposted_postid'].astype('str')

    # format dataframe
    df.sort_values(by = 'post_time', ascending=True, inplace=True)
    df = df[df['reposted_postid'].isnull() == False]
    df = df[df['accountid'].isnull() == False]

    # rename df columns to conincide with event log standards
    cols = ['time:timestamp', 'concept:name', 'case:concept:name', 'is_control']
    df.columns = cols

    # split the datasets on the is_control variable (True means uncoordinated)

    uncoordinated_df = df[df['is_control'] == True]
    coordinated_df = df[df['is_control'] == False]

    uncoordinated_df = uncoordinated_df.drop(columns='is_control')
    coordinated_df = coordinated_df.drop(columns = 'is_control')

    return uncoordinated_df, coordinated_df


def preprocess_log(df, log_length):

    # convert df to an event log
    log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)

    # initialise new event log
    trimmed_log = EventLog()

    # trim each trace in the event log so it is a max length of 10
    for trace in log:
        if len(trace) > 10:
            trimmed_trace = Trace()
            trimmed_trace.attributes.update(trace.attributes)
            for i in range(10):
                trimmed_trace.append(trace[i])
            trimmed_log.append(trimmed_trace)
        else:
            trimmed_log.append(trace)

    # remove traces of length 1
    filtered_log = filter_case_size(trimmed_log, 2, 1e6)

    # # select the first x traces
    short_log = EventLog()

    for i in range(log_length):
        short_log.append(filtered_log[i])

    return short_log


if __name__ == "__main__":
    from load_config import load_config
    import os
    import argparse
    import pm4py
    from pathlib import Path

    config = load_config()

    parser = argparse.ArgumentParser()
    parser.add_argument("--country", type=str, required=True, choices=["spain", "thailand"], help="Name of the country to load the dataset(s) for")
    args = parser.parse_args()

    # Construct dataset path
    dataset_paths = [str(p) for p in Path('data/raw_data').iterdir() if p.name.lower().startswith(args.country.lower()) and p.name.lower().endswith('.gzip.parquet')]

    # check if all paths exist
    for dataset_path in dataset_paths:
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    
    # concatenate all files
    df = pd.concat((pd.read_parquet(f, engine='pyarrow') for f in dataset_paths), ignore_index=True)

    # preprocess the df
    uncoordinated_df, coordinated_df = preprocess_df(df)

    # assign log_length for each country

    if args.country == "spain":
        log_length = 3000
    elif args.country == "thailand":
        log_length = 1500

    # generate and process the event log
    uncoordinated_log = preprocess_log(uncoordinated_df, log_length)
    coordinated_log = preprocess_log(coordinated_df, log_length)

    # save the event logs

    pm4py.write_xes(uncoordinated_log, os.path.join(config["project_root"], "data", args.country.lower() + "_uncoordinated.xes"))
    pm4py.write_xes(coordinated_log, os.path.join(config["project_root"], "data", args.country.lower() + "_coordinated.xes"))

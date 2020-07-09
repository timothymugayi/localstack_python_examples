import os
import time
import math
import pathlib
import numpy as np
import dask.dataframe as dd
import pandas as pd

from dask.distributed import Client, LocalCluster


os.environ['LOCALSTACK_S3_ENDPOINT_URL'] = 'http://localhost:4572'
BASE_DIR = pathlib.Path(__file__).parent.absolute()


def roundup(x, base: int = 5):
    """Round `x` up to nearest `base`"""
    return int(math.ceil(x / float(base))) * base


def round_series_up(s: dd.Series) -> dd.Series:
    """Apply roundup function to all elements of `s`"""
    return s.apply(roundup, meta=pd.Series(data=[], dtype=np.float32))


def transform_dask_dataframe(df: dd.DataFrame) -> dd.DataFrame:
    """Process NYC taxi data"""
    return (
        df[[
            'tpep_pickup_datetime', 'tpep_dropoff_datetime',
            'trip_distance', 'total_amount'
        ]]
        .astype({
            'tpep_pickup_datetime': 'datetime64[ms]',
            'tpep_dropoff_datetime': 'datetime64[ms]'
        })
        .assign(drive_time=(lambda df: (df.tpep_dropoff_datetime - df.tpep_pickup_datetime).dt.seconds // 300))
        .assign(drive_time=lambda df: round_series_up(df.drive_time))
        .assign(trip_distance=lambda df: round_series_up(df.trip_distance))
        .query('drive_time <= 120 & trip_distance <= 50')
        .drop(['tpep_pickup_datetime', 'tpep_dropoff_datetime'], axis=1)
        .round({'trip_distance': 0})
        .groupby(['drive_time', 'trip_distance'])
        .mean()
        .rename(columns={'total_amount': 'avg_amount'})
    )


def compute_final_dataframe(df: dd.DataFrame) -> pd.DataFrame:
    """Execute dask task graph and compute final results"""
    return (
        df
        .compute()
        .reset_index()
        .pivot(
             index='drive_time',
             columns='trip_distance',
             values='avg_amount'
        )
        .fillna(0)
    )

def run():

    # Lets toggle localstack by changing where boto3 is pointing to
    if os.environ.get('LOCALSTACK_S3_ENDPOINT_URL'):
        taxi_data = dd.read_csv( 's3://nyc-tlc/trip data/yellow_tripdata_2018-04_*.csv',
            storage_options={
                'anon': True,
                'use_ssl': False,
                'key': 'foo', 'secret': 'bar',
                "client_kwargs": {
                    "endpoint_url": os.environ.get('LOCALSTACK_S3_ENDPOINT_URL'),
                }
            }
        )
    else:
        # This assumes your using named profiles in aws cli with a default profile accessing your s3 bucket or EC2
        # instance or ECS task role
        taxi_data = dd.read_csv('s3://nyc-tlc/trip data/yellow_tripdata_2018-04_*.csv')

    taxi_data = transform_dask_dataframe(taxi_data)

    taxi_data = compute_final_dataframe(taxi_data)

    print(taxi_data)


# Generated table is the mean values of fares by distance and time

if __name__ == '__main__':

    # Connect to the appropriate dask cluster either local, self hosted or cloud provided
    # client = Client('tcp://localhost:8786| or cloud dask cluster URL (aws farget|saturncloud)')
    # cluster = LocalCluster(ip='0.0.0.0', n_workers=4, threads_per_worker=2, memory_limit='2G', dashboard_address='0.0.0.0:8787', processes=True)
    client = Client('tcp://localhost:8786')
    print('started dask Cluster...')
    print(client)
    print('waiting before process...')
    time.sleep(10)
    run()
    input("Press enter to exit...")



import duckdb
import pandas as pd
import numpy
import matplotlib.pyplot as plt


"""
              column_name column_type null   key default extra
0                VendorID      BIGINT  YES  None    None  None
1    tpep_pickup_datetime   TIMESTAMP  YES  None    None  None
2   tpep_dropoff_datetime   TIMESTAMP  YES  None    None  None
3         passenger_count      BIGINT  YES  None    None  None
4           trip_distance      DOUBLE  YES  None    None  None
5              RatecodeID      BIGINT  YES  None    None  None
6      store_and_fwd_flag     VARCHAR  YES  None    None  None
7            PULocationID      BIGINT  YES  None    None  None
8            DOLocationID      BIGINT  YES  None    None  None
9            payment_type      BIGINT  YES  None    None  None
10            fare_amount      DOUBLE  YES  None    None  None
11                  extra      DOUBLE  YES  None    None  None
12                mta_tax      DOUBLE  YES  None    None  None
13             tip_amount      DOUBLE  YES  None    None  None
14           tolls_amount      DOUBLE  YES  None    None  None
15  improvement_surcharge      DOUBLE  YES  None    None  None
16           total_amount      DOUBLE  YES  None    None  None
17   congestion_surcharge      DOUBLE  YES  None    None  None
18            airport_fee      DOUBLE  YES  None    None  None

"""


def graph_speed_by_day(input_parquet):
    query = f"""
    WITH speeds AS (
    SELECT
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        trip_distance,
        (EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)) / 60) AS duration_minutes,
        (trip_distance / NULLIF(EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)) / 3600, 0)) AS speed
        FROM read_parquet('{input_parquet}')
    )
    SELECT tpep_pickup_datetime::date as pickup_date, AVG(trip_distance) AS avg_trip_distance, AVG(duration_minutes) AS avg_duration_minutes, AVG(speed) AS avg_speed
    FROM speeds
    -- group by day
    GROUP BY tpep_pickup_datetime::date
    """

    df = duckdb.query(query).df()

    df["pickup_date"] = pd.to_datetime(df["pickup_date"])
    # Plot time series
    plt.figure()
    plt.plot(df["pickup_date"], df["avg_speed"])
    plt.xlabel("Date")
    plt.ylabel("Average Speed (mph)")
    plt.title("Average Daily Taxi Speed")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print(df)



def graph_speed_by_week(input_parquet):
    query = f"""
    WITH speeds AS (
    SELECT
        tpep_pickup_datetime,
        tpep_dropoff_datetime,
        trip_distance,
        (EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)) / 60) AS duration_minutes,
        (trip_distance / NULLIF(EXTRACT(EPOCH FROM (tpep_dropoff_datetime - tpep_pickup_datetime)) / 3600, 0)) AS speed
        FROM read_parquet('{input_parquet}')
    )
    SELECT DATE_TRUNC('week', tpep_pickup_datetime::date) as pickup_date, AVG(trip_distance) AS avg_trip_distance, AVG(duration_minutes) AS avg_duration_minutes, AVG(speed) AS avg_speed
    FROM speeds
    -- group by week
    GROUP BY DATE_TRUNC('week', tpep_pickup_datetime::date)
    """

    df = duckdb.query(query).df()

    df["pickup_date"] = pd.to_datetime(df["pickup_date"])
    # Plot time series
    plt.figure()
    plt.plot(df["pickup_date"], df["avg_speed"])
    plt.xlabel("Date")
    plt.ylabel("Average Speed (mph)")
    plt.title("Average Weekly Taxi Speed")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print(df)





graph_speed_by_day('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet')
graph_speed_by_week('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet')
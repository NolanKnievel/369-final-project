import duckdb
import pandas
import numpy

""""
Example Row: 
(2, '2018 Mar 10 11:04:35 AM', '2018 Mar 10 11:12:32 AM', 1, 1.31, 1, 'N', 151, 75, 2, 7.5, 0.0, 0.5, 0.0, 0.0, 0.3, 8.3)

Table description: 
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



def transform_data(input_csv):
    query = """
    COPY (SELECT * FROM read_csv_auto(?, thousands=',', ignore_errors=true))
    TO 'data/2019_Yellow_Taxi_Trip_Data.parquet' (FORMAT PARQUET);
    """

    duckdb.sql(query, params=[input_csv])


# # transform_data('data/2018_Yellow_Taxi_Trip_Data_20260214.csv')
# transform_data('data/2019_Yellow_Taxi_Trip_Data_20260219.csv')


# df = duckdb.sql("""SELECT * FROM read_parquet('data/2019_Yellow_Taxi_Trip_Data.parquet') LIMIT 10""").df()
# print(df)


def filter_data(input_parquet, output_parquet):
    print(f'filtering {input_parquet}')

    query = f"""
    COPY (
        WITH cleaned AS (
            SELECT *,
                strptime(tpep_pickup_datetime, '%Y %b %d %I:%M:%S %p') AS pickup_ts,
                strptime(tpep_dropoff_datetime, '%Y %b %d %I:%M:%S %p') AS dropoff_ts
            FROM read_parquet('{input_parquet}')
        )
        SELECT *
        FROM cleaned
        WHERE 
            dropoff_ts > pickup_ts
            AND (dropoff_ts - pickup_ts)
                BETWEEN INTERVAL 1 MINUTE AND INTERVAL 15 HOUR
            AND fare_amount > 0
            AND trip_distance > 0 AND trip_distance < 1000
            AND passenger_count > 0
            AND tip_amount > 0
    )
    TO '{output_parquet}' (FORMAT PARQUET);
    """

    duckdb.sql(query)


filter_data('data/2018_Yellow_Taxi_Trip_Data.parquet', 'data/parquet/2018_Filtered_Yellow_Taxi_Trip_Data.parquet')
import duckdb
import numpy
import pandas

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

def main():

    query = f"""
        SELECT *
        FROM read_csv('data/2018_Yellow_Taxi_Trip_Data_Sample.csv')
    """

    df = duckdb.query(query).df()
    print(df)


if __name__ == "__main__":
    main()

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
        SELECT tpep_pickup_datetime
        FROM read_csv_auto('data/samples/2019_Yellow_Taxi_Trip_Data_4th_July_Sample_V3.csv', thousands=',')
        ORDER BY tpep_pickup_datetime ASC
        LIMIT 1
    """

    df = duckdb.query(query).df()
    print(df)


if __name__ == "__main__":
    main()





"""

Slowest days 2019
july 3-7th
sept 2, 8th
april 21
may 25, 26
jan 21
feb 17th


Highest days 2019
jan 13, 16, 22
june 13
sept 11
Feb 2, 7, 28
april 13
march 6, 15


"""
import duckdb

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


# def create_sample(input_csv, output_csv, start_date, end_date):
#     print(f'creating random sample of {input_csv}')
    
#     query = f"""
#     COPY (
#         SELECT *
#         FROM read_csv_auto('{input_csv}', thousands=',')
#         WHERE 
#             -- ride time between 1 minute and 15 hours
#             tpep_dropoff_datetime > tpep_pickup_datetime
#             AND (tpep_dropoff_datetime - tpep_pickup_datetime) 
#                 BETWEEN INTERVAL 1 MINUTE AND INTERVAL 15 HOUR
            
#             -- fare amount positive
#             AND fare_amount > 0
            
#             -- trip distance bounds
#             AND trip_distance > 0
#             AND trip_distance < 1000
            
#             -- passenger count positive
#             AND passenger_count > 0
            
#             -- tip positive
#             AND tip_amount > 0

#             -- date filter
#             AND tpep_pickup_datetime >= CAST('{start_date}' AS TIMESTAMP)
#             AND tpep_dropoff_datetime < CAST('{end_date}' AS TIMESTAMP)

#         ORDER BY RANDOM()
#         LIMIT 20000
#     )
#     TO '{output_csv}'
#     WITH (HEADER, DELIMITER ',');
#     """



#     duckdb.sql(query)


def create_sample(input_parquet, output_csv, start_date, end_date, limit):
    print(f'creating random sample of {input_parquet}')
    
    query = f"""
    COPY (
        SELECT *
        FROM read_parquet('{input_parquet}')
        WHERE 
            -- ride time between 1 minute and 15 hours
            tpep_dropoff_datetime > tpep_pickup_datetime
            AND (tpep_dropoff_datetime - tpep_pickup_datetime) 
                BETWEEN INTERVAL 1 MINUTE AND INTERVAL 15 HOUR
            
            -- fare amount positive
            AND fare_amount > 0
            
            -- trip distance bounds
            AND trip_distance > 0
            AND trip_distance < 1000
            
            -- passenger count positive
            AND passenger_count > 0
            
            -- tip positive
            AND tip_amount > 0

            -- date filter
            AND tpep_pickup_datetime >= CAST('{start_date}' AS TIMESTAMP)
            AND tpep_dropoff_datetime < CAST('{end_date}' AS TIMESTAMP)

        ORDER BY RANDOM()
        LIMIT {limit}
    )
    TO '{output_csv}'
    WITH (HEADER, DELIMITER ',');
    """



    duckdb.sql(query)

"""
The following were the calls I made to create the samples used for analysis. 
When sampling single days, none of the limits were reached. 
"""
# NYE
# create_sample('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet', 'data/samples/2019_Yellow_Taxi_Trip_Data_New_Year_Sample.csv', '2019-12-31', '2020-01-01', 400_000)
# 4th of July
# create_sample('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet', 'data/samples/2019_Yellow_Taxi_Trip_Data_4th_July_Sample.csv', '2019-07-04', '2019-07-05' , 400_000)
# Yearlong
# create_sample('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet', 'data/samples/2019_Yellow_Taxi_Trip_Data_Sample.csv', '2019-01-01', '2020-01-01', 400_000)
# Random Tuesday in Nov
# create_sample('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet', 'data/samples/2019_Yellow_Taxi_Trip_Data_Sample_Tuesday.csv', '2019-11-19', '2019-11-20', 2_000_000)
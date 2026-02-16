import duckdb

def write_sample():
    print('creating random sample of 2018 data')
    
    query = f"""
    COPY (
        SELECT *
        FROM read_csv_auto('data/2018_Yellow_Taxi_Trip_Data_20260214.csv', thousands=',')
        ORDER BY RANDOM()
        LIMIT 13000
    )
    TO 'data/2018_Yellow_Taxi_Trip_Data_Sample.csv'
    WITH (HEADER, DELIMITER ',');
    """



    duckdb.query(query)



write_sample()
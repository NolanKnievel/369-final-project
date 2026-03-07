import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import calplot
# fix july compatibility
if not hasattr(matplotlib.cbook, "MatplotlibDeprecationWarning"):
    matplotlib.cbook.MatplotlibDeprecationWarning = matplotlib.MatplotlibDeprecationWarning

import july

"""
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



heatmap_query = f"""
    SELECT
        DATE(tpep_pickup_datetime) AS pickup_date,
        COUNT(*) AS total_trips
    FROM read_parquet('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet')
    WHERE YEAR(tpep_pickup_datetime) = 2019
    GROUP BY pickup_date
    ORDER BY pickup_date
"""

# heatmap of total traffic by day
def create_calendar_heatmap(): 
    # df = duckdb.sql(heatmap_query).df()

    # df["pickup_date"] = pd.to_datetime(df["pickup_date"])

    # # day of week
    # df["dow"] = df["pickup_date"].dt.dayofweek

    # # average rides for each weekday
    # dow_avg = df.groupby("dow")["total_trips"].transform("mean")

    # # deviation from expected weekday ridership
    # df["deviation"] = df["total_trips"] - dow_avg

    # ts = df.set_index("pickup_date")["deviation"]
    # # plot calendar heatmap
    # calplot.calplot(
    #     ts,
    #     cmap="coolwarm",
    #     figsize=(12,6),
    #     suptitle="NYC Yellow Taxi Trips per Day (2019)"
    # )

    # plt.show()

    df = duckdb.sql(heatmap_query).df()

    df["pickup_date"] = pd.to_datetime(df["pickup_date"])

    # day of week
    df["dow"] = df["pickup_date"].dt.dayofweek

    # weekday baseline
    dow_avg = df.groupby("dow")["total_trips"].transform("mean")

    # deviation from expected weekday ridership
    df["deviation"] = df["total_trips"] - dow_avg

    dates = df["pickup_date"]
    values = df["deviation"]

    plt.figure(figsize=(14,8))
    v = abs(values).max()
    values_norm = values / v
    july.calendar_plot(
        dates=dates,
        data=values_norm,
        cmap="coolwarm",
    )

    # plt.title("Deviation from Expected Taxi Ridership (NYC 2019)")
    plt.show()






create_calendar_heatmap()
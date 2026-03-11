import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import calplot
# july compatibility
if not hasattr(matplotlib.cbook, "MatplotlibDeprecationWarning"):
    matplotlib.cbook.MatplotlibDeprecationWarning = matplotlib.MatplotlibDeprecationWarning

import july





# heatmap of total traffic by day
def create_calendar_heatmap(): 
    heatmap_query = f"""
    SELECT
        DATE(tpep_pickup_datetime) AS pickup_date,
        COUNT(*) AS total_trips
    FROM read_parquet('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet')
    WHERE YEAR(tpep_pickup_datetime) = 2019
    GROUP BY pickup_date
    ORDER BY pickup_date
    """


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
    ax = plt.gca()

    v = abs(values).max()
    values_norm = values / v
    july.calendar_plot(
        dates=dates,
        data=values_norm,
        cmap="coolwarm",
    )

    # create legend manually
    norm = matplotlib.colors.Normalize(vmin=-v, vmax=v)
    sm = matplotlib.cm.ScalarMappable(norm=norm, cmap="coolwarm")
    sm.set_array([])

    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label("Deviation from Expected Taxi Trips")

    plt.show()

    # plt.title("Deviation from Expected Taxi Ridership (NYC 2019)")
    plt.show()


def create_zone_differences_sample(date_str): 
    print(f"Creating zone differences csvs for {date_str}")
    query1 = f"""
    COPY (
    WITH daily_zone_counts AS (
    SELECT
        DATE(tpep_pickup_datetime) AS pickup_date,
        PULocationID AS zone,
        COUNT(*) AS trips,
        EXTRACT(DOW FROM tpep_pickup_datetime) AS dow
    FROM read_parquet('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet')
    GROUP BY pickup_date, zone, dow
    ),
    zone_expected AS (
        SELECT
            zone,
            dow,
            AVG(trips) AS expected_trips
        FROM daily_zone_counts
        WHERE pickup_date <> DATE '{date_str}'
        GROUP BY zone, dow
    ),
    day_counts AS (
        SELECT
            zone,
            trips,
            dow
        FROM daily_zone_counts
        WHERE pickup_date = DATE '{date_str}'
    )

    SELECT
        dc.zone,
        dc.trips AS actual_trips,
        e.expected_trips,
        dc.trips - e.expected_trips AS deviation
    FROM day_counts dc
    JOIN zone_expected e
        ON dc.zone = e.zone AND dc.dow = e.dow)
    TO 'data/{date_str}_zone_pickup_differences.csv'
    WITH (HEADER, DELIMITER ',');
    """

    query2 = f"""
    COPY (
    WITH daily_zone_counts AS (
    SELECT
        DATE(tpep_dropoff_datetime) AS dropoff_date,
        PULocationID AS zone,
        COUNT(*) AS trips,
        EXTRACT(DOW FROM tpep_dropoff_datetime) AS dow
    FROM read_parquet('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet')
    GROUP BY dropoff_date, zone, dow
    ),
    zone_expected AS (
        SELECT
            zone,
            dow,
            AVG(trips) AS expected_trips
        FROM daily_zone_counts
        WHERE dropoff_date <> DATE '{date_str}'
        GROUP BY zone, dow
    ),
    day_counts AS (
        SELECT
            zone,
            trips,
            dow
        FROM daily_zone_counts
        WHERE dropoff_date = DATE '{date_str}'
    )

    SELECT
        dc.zone,
        dc.trips AS actual_trips,
        e.expected_trips,
        dc.trips - e.expected_trips AS deviation
    FROM day_counts dc
    JOIN zone_expected e
        ON dc.zone = e.zone AND dc.dow = e.dow)
    TO 'data/{date_str}_zone_dropoff_differences.csv'
    WITH (HEADER, DELIMITER ',');
    """


    duckdb.sql(query1)
    duckdb.sql(query2)



def create_hourly_demand_curve(dates):

    print(f"Creating hourly demand comparison for {dates}")

    date_list = ",".join([f"DATE '{d}'" for d in dates])

    query = f"""
    WITH hours AS (
        SELECT * FROM range(0,24) h(hour)
    ),

    hourly_counts AS (
        SELECT
            DATE(tpep_pickup_datetime) AS pickup_date,
            EXTRACT(DOW FROM tpep_pickup_datetime) AS dow,
            EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour,
            COUNT(*) AS trips
        FROM read_parquet('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet')
        GROUP BY pickup_date, dow, hour
    ),

    holiday_counts AS (
        SELECT
            pickup_date,
            hour,
            trips
        FROM hourly_counts
        WHERE pickup_date IN ({date_list})
    )

    SELECT *
    FROM holiday_counts
    """

    holiday_df = duckdb.sql(query).df()
    holiday_df["pickup_date"] = pd.to_datetime(holiday_df["pickup_date"])

    plt.figure(figsize=(12,7))

    # plot each holiday
    for d in dates:
        subset = holiday_df[holiday_df["pickup_date"] == pd.to_datetime(d)]
        subset = subset.sort_values("hour")

        plt.plot(
            subset["hour"],
            subset["trips"],
            linewidth=3,
            label=d
        )

    # average Monday
    # monday_df = duckdb.sql("""
    #     WITH daily_hour AS (
    #         SELECT
    #             DATE(tpep_pickup_datetime) AS d,
    #             EXTRACT(HOUR FROM tpep_pickup_datetime) AS hour,
    #             COUNT(*) AS trips
    #         FROM read_parquet('data/parquet/2019_Filtered_Yellow_Taxi_Trip_Data.parquet')
    #         WHERE EXTRACT(DOW FROM tpep_pickup_datetime) = 1
    #         GROUP BY d, hour
    #     )
    #     SELECT hour, AVG(trips) AS trips
    #     FROM daily_hour
    #     GROUP BY hour
    #     ORDER BY hour
    # """).df()

    # plt.plot(monday_df["hour"], monday_df["trips"],
    #          linestyle="--", linewidth=3, label="Avg Monday")

    plt.xlabel("Hour of Day")
    plt.ylabel("Trips")
    plt.title("Hourly Taxi Demand")

    plt.xticks(range(24))
    plt.grid(alpha=0.3)
    plt.legend()
    plt.ylim(0, 15_000)

    plt.show()


create_hourly_demand_curve(['2019-01-14', '2019-01-15', '2019-01-16', '2019-01-17', '2019-01-18', '2019-01-19', '2019-01-20'])


# I ran these calls to create csv samples for tableau
# create_zone_differences_sample("2019-12-25")
# create_zone_differences_sample("2019-12-31")
# create_zone_differences_sample("2019-01-01")
# create_zone_differences_sample("2019-10-31")
# create_zone_differences_sample("2019-01-01")



create_calendar_heatmap()

# holidays
create_hourly_demand_curve(["2019-07-04", "2019-12-25", "2019-11-28", "2019-12-31", "2019-01-01", "2019-10-31"])

# outlier days
create_hourly_demand_curve(["2019-03-25", "2019-02-18", "2019-05-27", "2019-09-02", "2019-10-14"])

# jan 14-21
create_hourly_demand_curve(["2019-01-14", "2019-01-15", "2019-01-16", "2019-01-17", "2019-01-18", "2019-01-19", "2019-01-20", "2019-01-21"])
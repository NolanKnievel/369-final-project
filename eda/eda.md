For this project I'm working with NYC Taxi record data from 2018. I did EDA on Tableau using a random sample of 13,000 rows from my 85 million row dataset.


### Elapsed Ride Time

We can create a calculated field to represent elapsed taxi ride time. I do this using Tableau's DateDiff function at minute-level precision.

The resulting distribution appears log-normal with its peak at 15-20 minutes, which sounds reasonable.

The following anomalies appeared. We'll exclude each of these...

There are some legit outliers. The main distrubution of ride times reaches up to 160 minutes. Beyond a large gap, there is also a small group of rides at around 1400 minute durations. All of these points are just shy of 24 hrs. Looking at their actual values, the dropoff time is always just before the pickup time, but the following day. My best guess is dropoff and pickup times got swapped.

There are 100 or so rides that have durations less than 1 minute.

There is one ride with a negative duration.

## Fare Amount

I created a histogram of fare amounts using $5 bins. The histogram appears reasonable with 5 and 10 dollar bins as the most popular. There are a number of negative fares so we will make sure to exclude these.

There are some outliers to the right. The greatest fare is one ride that cost $400. Though these are high, they could be within reason for a (very long) taxi ride so we will leave them for now. I'll have to do some experimentation with the full dataset to make sure there aren't any ridiculous fare amounts.

## Trip Distance

A histogram of trip distance also appears reasonable. Using 1-mile bins, we get the majority of trips occur within 1-2 miles, and then fall off pretty quickly after that. 

Similar to fare amount, there are some outliers to the right. The greatest trip distance is 92 miles, which seems reasonable. Once again, I'll check the max values of the entire dataset to make sure there is nothing out of reason.  

## Passenger Count

Our passenger count histogram looks reasonable, with the majority of rides just having 1 person. There are a small portion of rides with 0 people marked, so we will exclude these. 

## Tip Amount

Our tip amount histogram also appears reasonable. Most rides have $0-$2 tips. The largest tip in our sample is $50

## Fare vs distance
This graph appears to have a relatively strong, positive, linear relationship which checks out. Our 95 mile ride also has the highest fare price which also tracks. 

## Ride Hour Popularity

Graphing the number of rides each hour of the day gives min hours from 2-5 am and busy hours 9am-8pm. This absolutely makes sens. 

## Ride Day Popularity

Graphing taxi rides by day of week, ride counts increase throughout the week Monday-Friday/Saturday, and dramatically fall off Sunday. This also makes logical sense. 




## Verdict

Though we did find some data to exclude, this EDA has given me condifence in the validity of the taxi data since it passes logical checks. 
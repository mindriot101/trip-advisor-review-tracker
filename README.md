# Trip advisor review tracker

Download the review score breakdown for a trip advisor site.

## Usage

First find the url of the reviews to be tracked. Then decide if it's a hotel or attraction. Finally run the `fetch_latest.py` script passing these arguments. The results are then printed to stdout. Some example output:


```
excellent:100,very good:100,average:100,poor:100,terrible:100
```

These are the scores in reverse quality order.

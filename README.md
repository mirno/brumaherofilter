# brumaherofilter
Simple first concept to filter a dataset.
Data is required in csv format. Where it searched for the fields 'datum' and 'tijd'
```
iddatarows,datum,tijd,...
74765536,2023-12-20,23:59:41,102,...
```

# How to run
Install [Python3](https://www.python.org/downloads/).
Get python working on the command line.
Install [python pandas library](https://pandas.pydata.org/) using pip
> python -m pip install pandas
Create a data folder this git repo. (This will be ignored by git)
> mkdir data

## Example:
```
$ python pythonDataFilter.py
Enter input CSV file path (default: data/input.csv):
Enter output CSV file path (default: data/output.csv):
Choose delimiter - Comma (C) or Tab (T) [default: Comma]:
Choose time interval - Hourly (H) or Minutes (M) [default: Hourly]: M
Enter the number of minutes for interval: 10
Choose First (F) or Last (L) entry for each interval [default: First]: L
Processed data saved to data/output.csv
```

# Requirements
Python

Pandas which is a python module
> python -m pip install pandas

input.csv is where the data should be placed in csv format (",")
Easy trick is to ctrl+f in [notepad++](https://notepad-plus-plus.org/downloads/) and replace the tab fields for ",".
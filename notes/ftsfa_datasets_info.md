# FTSFA Datasets Info

## Storage
This note contains information about the FTSFA datasets.

All of the datasets are stored in the `DATA_DIR` directory, which is set to
`./_data` by default. Inside this directory, there is a `ftsfa_datasets.toml` file,
which contains the dataset key and the relative path to the dataset file.

The datasets are grouped by subfolder. For example, all of the NYU Call Report
datasets are stored in the `nyu_call_report` subfolder.

## Share
Each dataset looks like this:
```python
>>> print(df.head())
```
```
  entity       date      value
0      0 1976-03-31  13.497924
1      0 1976-06-30  13.936402
2      0 1976-09-30  13.412412
3      0 1976-12-31  14.272215
4      0 1977-03-31  13.654529
```

```python
>>> print(df.info())
```
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 833187 entries, 0 to 833186
Data columns (total 3 columns):
 #   Column  Non-Null Count   Dtype         
---  ------  --------------   -----         
 0   entity  833187 non-null  object        
 1   date    833187 non-null  datetime64[ns]
 2   value   833148 non-null  float64       
dtypes: datetime64[ns](1), float64(1), object(1)
memory usage: 19.1+ MB
None
```

The first column is the entity id, the second column is the date, and the third
column is the value. Each dataset is sorted by entity, then by date,
so that the dates are ordered within each entity.

### Explanation

This is the info that I used to determine the format of the datasets:
For panel data intended for time series forecasting in Python, the recommended structure and sorting approach is as follows:

_Recommended Column Order:_
- Entity (identifier), Date (timestamp), Value (target)

This ordering clearly separates each individual entity's time series, making it easier to manage and forecast multiple series simultaneously.

_Recommended Sorting:_
- First sort by Entity, then by Date.

Sorting first by entity ensures that all observations for each entity are grouped together. Sorting secondarily by date ensures that within each entity, observations are chronologically ordered. This sorting is crucial because time series forecasting methods rely on the correct temporal order of observations within each entity.

**Example:**
| Entity | Date       | Value |
|--------|------------|-------|
| A      | 2025-01-01 | 100   |
| A      | 2025-01-02 | 110   |
| A      | 2025-01-03 | 115   |
| B      | 2025-01-01 | 200   |
| B      | 2025-01-03 | 220   |

This format and sorting method will facilitate straightforward integration with common Python forecasting libraries such as Prophet, statsmodels, sktime, or darts, which typically assume data is provided in long format with explicit entity identifiers and chronological ordering.



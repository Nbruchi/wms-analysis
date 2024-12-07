# 🌿 **Wms Data Processing and Feature Engineering**

This project focuses on automating the process of collecting, cleaning, and processing data from waste management APIs to generate meaningful insights and features for analysis. It combines data from recycling events and schedule records, cleans the data, and performs feature engineering to extract useful insights.

## 📋 **Overview**

The script fetches two datasets from the local APIs:
1. **Recycling Data**: Contains information about waste recycling events, including the type and quantity of materials.
2. **Schedule Data**: Includes details about scheduled waste collection events, such as the time and frequency.

The script performs the following key steps:
- Data Collection: Fetches the raw data from the APIs.
- Data Cleaning: Handles missing values, duplicates, and ensures the data is ready for analysis.
- Feature Engineering: Extracts additional features such as differences in quantities and days between recycling events and their respective schedules.
- Data Analysis: Outputs summary statistics and feature insights for better decision-making.

---

## ⚙️ **Steps in the Script**

### 1. **Data Collection** 📡
The script retrieves data from two different API endpoints:
- **Recycles API**: Fetches recycling event data (type, quantity, and date).
- **Schedules API**: Fetches waste collection schedule data (time, frequency, and schedule ID).

```python
recycles_api = requests.get('http://127.0.0.1:8000/recycles/')
schedules_api = requests.get('http://127.0.0.1:8000/schedules/')
```

### 2. **Data Conversion to DataFrame** 📊
Once the data is fetched, it's converted into pandas DataFrames for easier manipulation and analysis.

```python
pdf = pd.DataFrame(recycles_api_data)
tdf = pd.DataFrame(schedules_api_data)
```

### 3. **Data Cleaning** 🧹
- **Null Values Check**: The script checks for any missing values and fills numeric columns with the mean value to avoid any data gaps.
- **Removing Duplicates**: Duplicate records are detected and removed to ensure data consistency.

```python
merged_df.fillna(merged_df.mean(numeric_only=True), inplace=True)
merged_df.drop_duplicates(inplace=True)
```

### 4. **Feature Engineering** 🔧
We generate new insights through feature engineering:
- **Quantity Difference**: Calculates the difference in quantity between recycling and schedule records.
- **Days Difference**: Computes the number of days between the recycling event date and the scheduled collection time.
- **Is Same Type**: A boolean indicator for whether the material types from recycling and schedules match.

```python
df['quantity_diff'] = df['quantity_x'] - df['quantity_y']
df['days_difference'] = (pd.to_datetime(df['date']) - pd.to_datetime(df['time'])).dt.days
df['is_same_type'] = (df['type_x'] == df['type_y']).astype(int)
```

### 5. **Output Results** 📈
The script outputs:
- **Summary Statistics**: Provides an overview of the dataset, including mean, standard deviation, min/max values, etc.
- **Column Information**: Details about the data types and non-null values.
- **Feature Analysis**: Summarizes the new features created for analysis.

---

## 📊 **Output Example**

Upon successful execution, the script prints detailed information about the dataset:

### Initial Shape
The dataset contains **500,000** rows and **9 columns**, showing the successful processing of large-scale data.

```
Initial Shape: (500000, 9)
```

### Null Values Check
It ensures no missing values in the dataset after filling them with appropriate defaults.

```
Null Values in Each Column:
type           0
quantity       0
date           0
schedule_id    0
...
```

### Summary Statistics
The dataset is summarized, showing descriptive statistics for all columns.

```
Summary Statistics:
           type       quantity        date
count    500000  500000.000000      500000
unique        5            NaN           2
...
```

### Column Information
Details about the dataset’s structure, including data types and memory usage.

```
Column Info:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 500000 entries, 0 to 499999
...
```

### Feature Analysis
Summary of the newly engineered features for deeper analysis.

```
Feature Analysis:
      quantity_diff  days_difference  is_same_type
count    500000    500000.0     500000.0
mean         NaN       330.0          0.23
...
```

---

## 🚀 **Key Features and Insights**

- **Efficient Data Processing**: Handles large datasets with 500,000 rows without performance degradation.
- **Data Quality Assurance**: Ensures clean data with automatic handling of missing values and duplicates.
- **Feature Engineering**: Adds valuable features like quantity differences and date mismatches for advanced analysis.
- **Customizable for Various Use Cases**: The script can be easily adapted to handle other datasets or features as needed.

---

## 📝 **Usage Instructions**

1. **Install Dependencies**:
   Ensure you have the necessary Python libraries installed:
   ```bash
   pip install pandas requests
   ```

2. **Run the Script**:
   Simply execute the script:
   ```bash
   python3 main.py
   ```

3. **Customize as Needed**:
   Modify the script to adapt it to different APIs, datasets, or features based on your project needs.
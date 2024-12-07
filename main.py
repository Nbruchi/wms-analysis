import requests
import pandas as pd

try:
    # Fetch data from APIs
    recycles_api = requests.get('http://127.0.0.1:8000/recycles/')
    recycles_api.raise_for_status()
    recycles_api_data = recycles_api.json()

    schedules_api = requests.get('http://127.0.0.1:8000/schedules/')
    schedules_api.raise_for_status()
    schedules_api_data = schedules_api.json()

    # No slicing; handling all data now
    # Uncomment for debugging:
    # print(recycles_api_data[:5])  
    # print(schedules_api_data[:5])

    # Convert API data to DataFrames
    pdf = pd.DataFrame(recycles_api_data)
    tdf = pd.DataFrame(schedules_api_data)

    # Parse date fields into datetime format and extract date only
    pdf['date'] = pd.to_datetime(pdf['date']).dt.date
    tdf['time'] = pd.to_datetime(tdf['time']).dt.date

    # Merge DataFrames based on schedule_id (in recycle) and id (in schedule)
    merged_df = pd.merge(pdf, tdf, left_on='schedule_id', right_on='id', how="inner")

    # Clean the data
    print("\nInitial Shape:", merged_df.shape)

    # Null Values Check
    print("Null Values in Each Column:")
    print(merged_df.isnull().sum())

    # Fill Missing Values (numeric only columns)
    merged_df.fillna(merged_df.mean(numeric_only=True), inplace=True)
    print("\nNull Values After Replacement:")
    print(merged_df.isnull().sum())

    # Remove duplicate rows
    duplicates = merged_df[merged_df.duplicated()]
    print(f"Number of duplicate rows: {len(duplicates)}")
    merged_df = merged_df.drop_duplicates()

    print("Duplicate rows removed.")
    print(f"Dataset shape after removing duplicates: {merged_df.shape}")

    # Feature Engineering
    def feature_engineering(df):
        # Feature 1: Quantity difference (if applicable)
        if 'quantity_x' in df.columns and 'quantity_y' in df.columns:
            df['quantity_diff'] = df['quantity_x'] - df['quantity_y']

        # Feature 2: Days difference between dates
        df['days_difference'] = (pd.to_datetime(df['date']) - pd.to_datetime(df['time'])).dt.days

        # Feature 3: Is same type (if applicable)
        if 'type_x' in df.columns and 'type_y' in df.columns:
            df['is_same_type'] = (df['type_x'] == df['type_y']).astype(int)

        return df

    merged_df = feature_engineering(merged_df)

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")

# Summary Statistics
print("Summary Statistics:")
print(merged_df.describe(include='all'))

# Column Info
print("\nColumn Info:")
print(merged_df.info())

# First Few Rows
print("\nFirst Few Rows:")
print(merged_df.head())

# Feature Analysis
if 'quantity_diff' in merged_df.columns and 'days_difference' in merged_df.columns:
    print("\nFeature Analysis:")
    print(merged_df[['quantity_diff', 'days_difference', 'is_same_type']].describe())

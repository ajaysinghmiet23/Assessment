import pandas as pd
import numpy as np

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    for idx in car_matrix.index:
        car_matrix.at[idx, idx] = 0

    return car_matrix
    


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    labels = ['low', 'medium', 'high']
    df['car_type'] = np.select(conditions, labels, default=np.nan)
    type_counts = df.groupby('car_type').size().sort_index().to_dict()
    sorted_type_counts = dict(sorted(type_counts.items()))
    return sorted_type_counts

    


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean = df['bus'].mean()
    filtered_df = df.query('bus > @bus_mean * 2')
    bus_indexes = filtered_df.index.tolist()

    return bus_indexes


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    avg_truck_by_route = pd.pivot_table(df, values='truck', index='route', aggfunc='mean')
    selected_routes = avg_truck_by_route[avg_truck_by_route['truck'] > 7].index.tolist()
    selected_routes.sort()

    return selected_routes


    

    


def multiply_matrix(df)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = generate_car_matrix(df).copy(deep=True)
    for idx in modified_matrix.index:
        for col in modified_matrix.columns:
            if modified_matrix.at[idx, col] > 20:
                modified_matrix.at[idx, col] *= 0.75
            else:
                modified_matrix.at[idx, col] *= 1.25
    modified_matrix = modified_matrix.round(1)

    return modified_matrix    

    


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S', errors='coerce')
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S', errors='coerce')
    completeness_check = (
        (df['end_datetime'] - df['start_datetime'] == pd.Timedelta(days=1)) &  # Covers 24 hours
        (df['start_datetime'].dt.day_name() == df['end_datetime'].dt.day_name())  # Spans all 7 days
    )
    result = df.groupby(['id', 'id_2'])['start_datetime', 'end_datetime'].apply(lambda x: all(completeness_check[x.index]))

    return result

df = pd.read_csv(r"C:\Users\LENOVO\Desktop\Assessment\MapUp-Data-Assessment-F\datasets\dataset-1.csv")
df2 = pd.read_csv(r"C:\Users\LENOVO\Desktop\Assessment\MapUp-Data-Assessment-F\datasets\dataset-2.csv")
print(multiply_matrix(df).head())


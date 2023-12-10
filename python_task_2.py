import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import numpy as np


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distances_dict = {}

    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        # Extract start and end IDs
        start_id, end_id = row['id_start'], row['id_end']

        # Get the distance between start and end IDs
        distance = row['distance']

        # Update cumulative distances for both directions
        distances_dict[(start_id, end_id)] = distances_dict.get((start_id, end_id), 0) + distance
        distances_dict[(end_id, start_id)] = distances_dict.get((end_id, start_id), 0) + distance

    # Create a list of unique toll IDs
    unique_ids = sorted(list(set(df['id_start'].unique()) | set(df['id_end'].unique())))

    # Initialize an empty matrix with zeros
    distance_matrix = pd.DataFrame(0, index=unique_ids, columns=unique_ids)

    # Populate the matrix with cumulative distances
    for start_id in unique_ids:
        for end_id in unique_ids:
            if (start_id, end_id) in distances_dict:
                distance_matrix.at[start_id, end_id] = distances_dict[(start_id, end_id)]

    return distance_matrix


    


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    distance_matrix = calculate_distance_matrix(df)
    unrolled_data = []

    # Iterate through the rows and columns of the distance matrix
    for start_id in distance_matrix.index:
        for end_id in distance_matrix.columns:
            # Exclude same start and end IDs
            if start_id != end_id:
                distance = distance_matrix.at[start_id, end_id]
                unrolled_data.append({'id_start': start_id, 'id_end': end_id, 'distance': distance})
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df



def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df
df = pd.read_csv(r"MapUp-Data-Assessment-F/datasets/dataset-3.csv")
print(unroll_distance_matrix(df).head())
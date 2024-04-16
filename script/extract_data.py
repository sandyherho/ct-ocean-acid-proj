#!/usr/bin/env python

"""
extract_data.py
Extract time series & spatial data in Coral Triangle

Author: Sandy Herho
Email: sandy.herho@email.ucr.edu
Date: 04/10/2024
"""

import xarray as xr
import pandas as pd

def load_and_select(filepath, lon_range, lat_range):
    """
    Load a NetCDF file and select a subset of the data within the specified longitude and latitude ranges.

    Parameters:
    - filepath: str, path to the NetCDF file.
    - lon_range: tuple, the longitude range to select.
    - lat_range: tuple, the latitude range to select.

    Returns:
    - xarray Dataset with the selected subset of data.
    """
    return xr.open_dataset(filepath).sel(lon=slice(*lon_range), lat=slice(*lat_range))

def process_and_save(scenario, base_path, save_path_processed, save_path_temporal):
    """
    Process and save the data for a given climate scenario by loading the data,
    calculating the mean across specified dimensions, and saving the result to a CSV file.

    Parameters:
    - scenario: str, the name of the scenario to process (e.g., 'historical', 'ssp119').
    - base_path: str, the base directory containing the dataset.
    - save_path_processed: str, the directory to save the processed NetCDF files.
    - save_path_temporal: str, the directory to save the summarized CSV files.
    """
    file_vars = ['pHT', 'Aragonite', 'Calcite']
    data_vars = ['pHT', 'aragonite', 'calcite']
    combined_data = {}
    time_collected = False

    for file_var, data_var in zip(file_vars, data_vars):
        med_file = f'{base_path}/{scenario}/{file_var}_median_{scenario}.nc'
        std_file = f'{base_path}/{scenario}/{file_var}_std_{scenario}.nc'
        
        med = load_and_select(med_file, (71, 172), (65, 119))
        std = load_and_select(std_file, (71, 172), (65, 119))

        # Save the NetCDF files after selection
        med.to_netcdf(f"{save_path_processed}/{scenario}_{file_var.lower()}_med.nc")
        std.to_netcdf(f"{save_path_processed}/{scenario}_{file_var.lower()}_std.nc")
        
        # Aggregate the data and store it in combined_data dictionary
        combined_data[f"{data_var}_med"] = med[data_var].mean(dim=("lat", "lon")).to_numpy()
        combined_data[f"{data_var}_std"] = std[data_var].mean(dim=("lat", "lon")).to_numpy()

        if not time_collected:
            combined_data['time'] = med["time"].to_numpy()
            time_collected = True

    # Save the aggregated data to a CSV file
    df = pd.DataFrame(combined_data)
    df.to_csv(f"{save_path_temporal}/{scenario}.csv", index=False)

def main():
    """
    Main function to process and save datasets for different climate scenarios.
    """
    # Define the base path for the input data and the paths for saving processed data
    base_path = '../data/pre_processed/acid'
    save_path_processed = '../data/processed/spa'
    save_path_temporal = '../data/processed/temporal'

    # List of scenarios to process
    scenarios = ['historical', 'ssp119', 'ssp126', 'ssp245', 'ssp370', 'ssp585']
    
    for scenario in scenarios:
        process_and_save(scenario, base_path, save_path_processed, save_path_temporal)

if __name__ == "__main__":
    main()


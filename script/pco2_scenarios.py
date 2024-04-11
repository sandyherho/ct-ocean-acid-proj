#!/usr/bin/env python

"""
pco2_scenarios.py

Plotting CMIP6 pCO2 scenarios

Author: Sandy Herho
Email: sandy.herho@email.ucr.edu
Date: 03/29/2024
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("bmh")

class ClimateDataAnalyzer:
    """
    A class for analyzing and plotting climate data.
    """

    def __init__(self, file_paths):
        """
        Initializes the ClimateDataAnalyzer with file paths.

        Parameters:
            file_paths (dict): A dictionary mapping dataset names to file paths.
        """
        self.file_paths = file_paths
        self.data_frames = {}
        self.stats = {}

    def load_data(self, file_path):
        """
        Loads climate data from a CSV file and limits it to the year 2100.

        Parameters:
            file_path (str): The file path to load the data from.

        Returns:
            pd.DataFrame: The loaded and filtered data frame.
        """
        df = pd.read_csv(file_path, usecols=["year", "data_mean_global"])
        df = df[df["year"] <= 2100]  # Filter data to include only years up to 2100
        return df

    def find_max_min_values(self, df):
        """
        Finds the max and min values in the 'data_mean_global' column of a DataFrame.

        Parameters:
            df (pd.DataFrame): The data frame to analyze.

        Returns:
            dict: A dictionary with the max and min values and corresponding years.
        """
        max_value = df['data_mean_global'].max()
        min_value = df['data_mean_global'].min()
        max_year = df.loc[df['data_mean_global'].idxmax(), 'year']
        min_year = df.loc[df['data_mean_global'].idxmin(), 'year']
        return {'max_value': max_value, 'max_year': max_year, 'min_value': min_value, 'min_year': min_year}

    def process_data(self):
        """
        Loads and processes the data for each dataset specified in file_paths.
        """
        for name, path in self.file_paths.items():
            df = self.load_data(path)
            self.data_frames[name] = df
            self.stats[name] = self.find_max_min_values(df)

    def plot_data(self):
        """
        Plots the climate data for all datasets.
        """
        plt.figure(figsize=(10, 6))
        ax = plt.gca()  # Get the current axis

        for name, df in self.data_frames.items():
            ax.plot(df["year"], df["data_mean_global"], label=name)

        ax.legend(loc="upper left")
        ax.set_xlabel("Time [years]", fontsize=18)
        ax.set_ylabel(r"pCO$_2$ [ppm]", fontsize=18)
        plt.tight_layout()
        plt.xlim(-1, 2102)
        plt.savefig("../figs/fig2.png", dpi=400)

if __name__ == "__main__":
    file_paths = {
        "Historical": "../data/rf/historical.csv",
        "SSP 1.19": "../data/rf/IMAGE_ssp119.csv",
        "SSP 1.26": "../data/rf/IMAGE_ssp126.csv",
        "SSP 2.45": "../data/rf/MASSAGE_GLOBIOM_ssp245.csv",
        "SSP 3.70": "../data/rf/AIM_ssp370.csv",
        "SSP 5.85": "../data/rf/REMIND_MAGPIE_ssp585.csv"
    }

    analyzer = ClimateDataAnalyzer(file_paths)
    analyzer.process_data()
    analyzer.plot_data()

    # Print statistics, if necessary
    for name, stat in analyzer.stats.items():
        print(f"{name} statistics:\n{stat}\n")

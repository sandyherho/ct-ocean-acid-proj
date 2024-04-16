#!/usr/bin/env python

"""
temp_plot.py

Time Series Plot

Author: Sandy Herho
Email: sandy.herho@email.ucr.edu
Date: 04/15/2024
"""
import pandas as pd
import matplotlib.pyplot as plt

class ClimateDataPlotter:
    """
    A class to plot climate data including pH, aragonite, and calcite from different scenarios.
    
    Attributes:
        data_paths (dict): Dictionary of file paths for each data scenario.
        style (str): Matplotlib style to be used for plots.
        output_dir (str): Directory to save plots.
    """
    def __init__(self, data_paths, style='bmh', output_dir='../figs/'):
        """
        Initializes the ClimateDataPlotter with paths to the data files, plot style, and output directory.
        """
        self.data_paths = data_paths
        self.style = style
        self.output_dir = output_dir
        plt.style.use(self.style)

    def load_data(self):
        """
        Loads data from the specified paths and stores them in a dictionary.
        
        Returns:
            dict: A dictionary of dataframes for each scenario.
        """
        return {key: pd.read_csv(path) for key, path in self.data_paths.items()}

    def plot_data(self, data, variable, variable_label):
        """
        Plots the given variable for all climate scenarios.

        Parameters:
            data (dict): A dictionary of pandas DataFrames containing the climate data.
            variable (str): The variable to plot (e.g., 'pH_med').
            variable_label (str): The label for the variable (for y-axis).
        """
        fig, ax = plt.subplots()
        for scenario, df in data.items():
            ax.plot(df["time"], df[variable], label=scenario)
            ax.fill_between(df["time"], df[variable] - 1.96*df[f"{variable[:-4]}_std"],
                            df[variable] + 1.96*df[f"{variable[:-4]}_std"], alpha=0.2)
        
        ax.set_xlabel("Time [Decades]", fontsize=18)
        ax.set_ylabel(variable_label, fontsize=18)
        ax.set_xlim(data['Historical']["time"].min(), data['SSP 1-1.9']["time"].max())
        ax.legend()
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        plt.savefig(f'{self.output_dir}{variable}.png', dpi=450)
        plt.show()

# Example usage
data_paths = {
    "Historical": "../data/processed/temporal/historical.csv",
    "SSP 1-1.9": "../data/processed/temporal/ssp119.csv",
    "SSP 1-2.6": "../data/processed/temporal/ssp126.csv",
    "SSP 2-4.5": "../data/processed/temporal/ssp245.csv",
    "SSP 3-7.0": "../data/processed/temporal/ssp370.csv",
    "SSP 5-8.5": "../data/processed/temporal/ssp585.csv"
}

plotter = ClimateDataPlotter(data_paths)
data = plotter.load_data()
plotter.plot_data(data, 'pH_med', 'pH')
plotter.plot_data(data, 'aragonite_med', r'$\Omega_{\text{Aragonite}}$')
plotter.plot_data(data, 'calcite_med', r'$\Omega_{\text{Calcite}}$')
#!/usr/bin/env python

"""
temp_stats.py
Temporal Statistics

Author: Sandy Herho
Email: sandy.herho@email.ucr.edu
Date: 03/29/2024
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from statsmodels.tsa.stattools import adfuller
import scikit_posthocs as sp

# Set visual style for all matplotlib plots
plt.style.use("bmh")

# Load data from CSV files
def load_data(file_path, column_name):
    return pd.read_csv(file_path)[column_name]

# File paths for the datasets
file_paths = {
    'Historical': '../data/processed/temporal/historical.csv',
    'SSP119': '../data/processed/temporal/ssp119.csv',
    'SSP126': '../data/processed/temporal/ssp126.csv',
    'SSP245': '../data/processed/temporal/ssp245.csv',
    'SSP370': '../data/processed/temporal/ssp370.csv',
    'SSP585': '../data/processed/temporal/ssp585.csv'
}

# Load specified column for each scenario
def load_datasets(file_paths, column_name):
    return {scenario: load_data(path, column_name) for scenario, path in file_paths.items()}

# Statistical analysis function
def analyze_data(data):
    data = data.dropna()  # Ensure no NA values interfere with calculations
    skew = stats.skew(data)
    kurt = stats.kurtosis(data, fisher=False)
    shapiro_stat, shapiro_p = stats.shapiro(data)
    adf_stat, adf_p, usedlag, nobs, critical_values, icbest = adfuller(data)
    return skew, kurt, shapiro_stat, shapiro_p, adf_stat, adf_p, critical_values

# Display statistical results
def display_results(scenario, results):
    print(f"\nResults for {scenario}:")
    skew, kurt, shapiro_stat, shapiro_p, adf_stat, adf_p, critical_values = results
    print(f"  Skewness: {skew:.3f}")
    print(f"  Kurtosis: {kurt:.3f}")
    print(f"  Shapiro-Wilk Test: Statistic={shapiro_stat:.3f}, p-value={shapiro_p:.3f}")
    print(f"  ADF Test: Statistic={adf_stat:.3f}, p-value={adf_p:.3f}, Critical Values={critical_values}")

# Function to prepare data for statistical testing
def prepare_data_for_testing(file_paths, column_name):
    data = [load_data(path, column_name) for path in file_paths.values()]
    labels = list(file_paths.keys())
    data_stacked = np.concatenate(data)
    groups = np.concatenate([[label] * len(d) for d, label in zip(data, labels)])
    return pd.DataFrame({'Value': data_stacked, 'Group': groups}), labels

# Function to perform Kruskal-Wallis and Dunn's tests
def perform_statistical_tests(df, labels, alpha=0.05):
    # Kruskal-Wallis test
    kw_stat, kw_pvalue = stats.kruskal(*[df[df['Group'] == label]['Value'] for label in labels])
    print(f'Kruskal-Wallis test statistic: {kw_stat:.3f}, p-value: {kw_pvalue:.3f}')

    if kw_pvalue < alpha:
        print("Significant differences found among the groups.")
        # Dunn's post-hoc test with Bonferroni adjustment
        dunn_pvalues = sp.posthoc_dunn(df, val_col='Value', group_col='Group', p_adjust='bonferroni')
        print(dunn_pvalues.round(3))
        # Plot heatmap of Dunn's test results
        plt.figure(figsize=(10, 8))
        sns.heatmap(dunn_pvalues, cmap='coolwarm_r', xticklabels=labels, yticklabels=labels)
        plt.show()

# Function to plot boxplots
def plot_results(df, labels, filename):
    plt.figure(figsize=(10, 8))
    sns.boxplot(x='Group', y='Value', data=df)
    plt.xticks(ticks=np.arange(len(labels)), labels=labels, rotation=45)
    plt.savefig(filename)

# Prepare and plot data
def prepare_and_plot_data(file_paths, column_name, file_prefix):
    data = load_datasets(file_paths, column_name)
    for scenario, dataset in data.items():
        results = analyze_data(dataset)
        display_results(scenario, results)
    df, labels = prepare_data_for_testing(file_paths, column_name)
    perform_statistical_tests(df, labels)
    plot_results(df, labels, f'../figs/{file_prefix}_boxplot.png')
    plot_density(data, labels, f'../figs/{file_prefix}_density.png')

# Plot density for each scenario
def plot_density(data, labels, filename):
    plt.figure(figsize=(10, 8))
    for label, dataset in data.items():
        sns.kdeplot(dataset.dropna(), label=label)
    plt.legend()
    plt.savefig(filename)

if __name__ == "__main__":
    # Analyze and plot for 'aragonite_med'
    prepare_and_plot_data(file_paths, 'aragonite_med', 'aragonite_med')

    # Analyze and plot for 'calcite_med'
    prepare_and_plot_data(file_paths, 'calcite_med', 'calcite_med')

    # Analyze and plot for 'pH_med'
    prepare_and_plot_data(file_paths, 'pH_med', 'pH_med')
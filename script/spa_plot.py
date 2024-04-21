#!/usr/bin/env python

"""
spa_plot.py

Plot Spatial

Sandy Herho <sandy.herho@email.ucr.edu>
04/20/24
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import scipy.stats as stats
import scikit_posthocs as sp

plt.style.use('bmh')

# Function to load dataset and select data
def load_and_select_data(filepath, variable, time=None, mean_dim=None):
    """
    Load data from a NetCDF file, select a variable and optionally select a specific time or average over a dimension.
    """
    ds = xr.open_dataset(filepath)
    data = ds[variable]
    if time:
        data = data.sel(time=time)
    if mean_dim:
        data = data.mean(dim=mean_dim)
    return data

# Function to plot data
def plot_data(data, bounds, filename, label, delta=False, vmin=None, vmax=None):
    """
    Plot 2D geographical data with a colormap, including a colorbar and annotations.
    """
    plt.figure(figsize=(10, 5))
    cmap = plt.cm.coolwarm_r.copy()
    cmap.set_bad('#402206')
    im = plt.imshow(data, extent=[bounds[1].min(), bounds[1].max(), bounds[0].min(), bounds[0].max()],
                    cmap=cmap, aspect='auto', origin='lower', vmin=vmin, vmax=vmax)
    cbar = plt.colorbar(im, label=label, boundaries=np.linspace(vmin, vmax, 8) if delta else None)
    cbar.set_label(label, size=15)
    cbar.ax.tick_params(labelsize=12)
    plt.xlabel('Longitude', fontsize=14)
    plt.ylabel('Latitude', fontsize=14)
    plt.savefig(filename, dpi=450)
    plt.close()

def main():
    # Variables and file paths
    variables = ["pHT", "aragonite", "calcite"]
    times = [None, "2100", "2100"]
    means = ["time", None, None]
    prefixes = ["ph", "ar", "cal"]
    suffixes = ["his", "ssp119", "ssp126", "ssp245", "ssp370", "ssp585"]
    base_path = "../data/processed/spa"

    # Loop through each variable
    for prefix, variable, time, mean in zip(prefixes, variables, times, means):
        datasets = {}
        for suffix in suffixes:
            path = f"{base_path}/{suffix}_{prefix}_med.nc"
            data = load_and_select_data(path, variable, time=time, mean_dim=mean)
            datasets[suffix] = data
        
        # Process historical data
        his_data = datasets["his"].to_numpy()
        lat_bounds = np.linspace(-25, 29, his_data.shape[0])
        lon_bounds = np.linspace(95, 196, his_data.shape[1])
        bounds = [lat_bounds, lon_bounds]

        # Plot historical data
        plot_data(his_data, bounds, f'../figs/fig_{prefix}6a.png', f'{variable} (Historical)')

        # Process projections and anomalies
        for i, suffix in enumerate(suffixes[1:], start=1):
            proj_data = datasets[suffix].to_numpy()
            anomaly = datasets[suffix] - datasets["his"]
            anomaly_data = anomaly.to_numpy()
            plot_data(anomaly_data, bounds, f'../figs/fig_{prefix}6{chr(i + 96)}.png',
                      r'$\Delta${}'.format(variable), delta=True, vmin=-0.6, vmax=-0.04)

        # Perform statistical analysis if needed
        control = his_data.flatten()[~np.isnan(his_data.flatten())]
        test_datasets = [datasets[s].to_numpy().flatten()[~np.isnan(datasets[s].to_numpy().flatten())] for s in suffixes[1:]]
        data = [control] + test_datasets
        stat, p_value = stats.kruskal(*data)
        if p_value < 0.05:
            p_values_matrix = sp.posthoc_dunn(data, p_adjust='bonferroni')
            print(f"Dunn's Test pairwise p-values with Bonferroni correction for {prefix}:\n", p_values_matrix)

if __name__ == "__main__":
    main()


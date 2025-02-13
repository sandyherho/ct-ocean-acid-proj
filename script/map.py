#!/usr/bin/env python

"""
map.py
Location of study map

Author: Sandy Herho
Email: sandy.herho@email.ucr.edu
Date: 03/29/2024
"""

import pygmt


class SRTMMapPlotter:
    """
    A class to encapsulate the process of loading, plotting, and saving SRTM15+ Earth relief data using PyGMT.

    Attributes:
        region (list): The geographical region to plot specified as [west, east, south, north].
        resolution (str): The resolution of the Earth relief data. Default is "15s".
        grid (xarray.DataArray): The loaded Earth relief data for the specified region.
        figure (pygmt.Figure): The PyGMT figure object for plotting.

    Methods:
        load_data(): Loads the Earth relief data based on the specified region and resolution.
        plot_map(): Plots the Earth relief data as a map.
        plot_marker(x, y, style, fill): Marks a specific point on the map.
        add_colorbar(frame): Adds a colorbar to the map.
        show(): Displays the figure in an interactive window.
        save(filename, dpi): Saves the figure to a file with the specified resolution.
    """

    def __init__(self, region, resolution="15s"):
        """
        Initializes the SRTMMapPlotter object with a specified region and resolution.

        Parameters:
            region (list): The geographical region to plot specified as [west, east, south, north].
            resolution (str): The resolution of the Earth relief data. Default is "15s".
        """
        self.region = region
        self.resolution = resolution
        self.grid = self.load_data()
        self.figure = pygmt.Figure()

    def load_data(self):
        """
        Loads the Earth relief data for the specified region and resolution.

        Returns:
            xarray.DataArray: The loaded Earth relief data.
        """
        return pygmt.datasets.load_earth_relief(
            resolution=self.resolution, region=self.region
        )

    def plot_map(self):
        """
        Plots the Earth relief data as a map using the loaded grid data.
        """
        self.figure.grdimage(grid=self.grid, projection="M15c", frame="a", cmap="geo")

    def plot_marker(self, x, y, style="c0.3c", fill="red"):
        """
        Marks a specific point on the map with a marker.

        Parameters:
            x (float): The longitude of the point to mark.
            y (float): The latitude of the point to mark.
            style (str): The style of the marker. Default is "c0.3c".
            fill (str): The fill color of the marker. Default is "red".
        """
        self.figure.plot(x=x, y=y, style=style, fill=fill)

    def add_colorbar(self, frame=["a2000", "x+lElevation", "y+lm"]):
        """
        Adds a colorbar to the map to indicate elevation values.

        Parameters:
            frame (list): Customization options for the colorbar. Default shows elevation in meters.
        """
        self.figure.colorbar(frame=frame)

    def show(self):
        """
        Displays the figure in an interactive window.
        """
        self.figure.show()

    def save(self, filename="../figs/fig1.png", dpi=400):
        """
        Saves the figure to a file with the specified resolution.

        Parameters:
            filename (str): The path and name of the file to save the figure.
            dpi (int): The resolution in dots per inch (DPI) for the saved figure. Default is 400.
        """
        self.figure.savefig(filename, dpi=dpi)


# CT map
if __name__ == "__main__":
    # Initialize the plotter with a specific geographical region
    plotter = SRTMMapPlotter(region=[95, 191, -25, 30])
    # Plot the Earth relief map
    plotter.plot_map()
    # Add a colorbar to the map
    plotter.add_colorbar()
    # Display the map
    plotter.show()
    # Save the map to a file
    plotter.save()

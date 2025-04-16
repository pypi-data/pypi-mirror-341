import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")  # Use the Qt5Agg backend for PyQt5
import matplotlib.pyplot as plt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QGroupBox, QSplitter, QLineEdit, QPushButton, QCheckBox,
    QComboBox, QMessageBox, QFileDialog, QSizePolicy
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import xarray as xr
from datetime import datetime
from ..plot_gen import plt_lev_var
from ..io import load_datasets, save_output
from ..data_parse import time_list, var_list, level_list, lon_list, lat_list


# ============================================================================
# Main GUI Window with an improved layout using QSplitter and QGroupBox
# ============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Level vs Variable Plotter")
        self.resize(1200, 600)  # Increase window size

        # Main splitter divides the window into a left (controls) and right (plot) panel.
        self.splitter = QSplitter(Qt.Horizontal)

        # -----------------------------------
        # Left Panel: Options & Controls
        # -----------------------------------
        self.options_widget = QWidget()
        self.options_layout = QVBoxLayout(self.options_widget)

        # Group box for dataset selection.
        self.dataset_group = QGroupBox("Dataset Selection")
        ds_layout = QFormLayout()
        self.directory_input = QLineEdit()
        self.directory_input.setPlaceholderText("Enter directory or file path")
        ds_layout.addRow("Directory:", self.directory_input)
        self.dataset_filter_input = QLineEdit()
        self.dataset_filter_input.setPlaceholderText("Optional filter (e.g., 'prim')")
        ds_layout.addRow("Dataset Filter:", self.dataset_filter_input)
        self.load_button = QPushButton("Load Datasets")
        self.load_button.clicked.connect(self.on_load_datasets)
        ds_layout.addRow(self.load_button)
        self.dataset_group.setLayout(ds_layout)
        self.options_layout.addWidget(self.dataset_group)

        # Group box for plot parameter options.
        self.param_group = QGroupBox("Plot Parameters")
        param_form = QFormLayout()
        self.var_combo = QComboBox()
        param_form.addRow("Variable Name:", self.var_combo)
        self.time_combo = QComboBox()
        param_form.addRow("Time (ISO):", self.time_combo)
        self.lat_combo = QComboBox()
        param_form.addRow("Latitude:", self.lat_combo)
        self.lon_combo = QComboBox()
        param_form.addRow("Longitude:", self.lon_combo)
        # Removed mtime input as requested.
        self.unit_input = QLineEdit()
        param_form.addRow("Variable Unit:", self.unit_input)
        self.level_min_input = QLineEdit()
        param_form.addRow("Level Minimum:", self.level_min_input)
        self.level_max_input = QLineEdit()
        param_form.addRow("Level Maximum:", self.level_max_input)
        self.log_level_checkbox = QCheckBox()
        self.log_level_checkbox.setChecked(True)
        param_form.addRow("Log Level:", self.log_level_checkbox)
        self.clean_plot_checkbox = QCheckBox()
        param_form.addRow("Clean Plot:", self.clean_plot_checkbox)
        self.verbose_checkbox = QCheckBox()
        param_form.addRow("Verbose:", self.verbose_checkbox)
        self.param_group.setLayout(param_form)
        self.options_layout.addWidget(self.param_group)

        # Buttons for refreshing lists and plotting.
        self.buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(self.buttons_widget)
        self.refresh_button = QPushButton("Refresh Valid Lists")
        self.refresh_button.clicked.connect(self.populate_combo_boxes)
        buttons_layout.addWidget(self.refresh_button)
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.on_plot)
        buttons_layout.addWidget(self.plot_button)
        self.options_layout.addWidget(self.buttons_widget)

        self.options_layout.addStretch()  # Push options to the top.

        # -----------------------------------
        # Right Panel: Plot Display
        # -----------------------------------
        self.plot_widget = QWidget()
        self.plot_layout = QVBoxLayout(self.plot_widget)
        self.canvas = FigureCanvas(plt.figure(figsize=(10, 6)))
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plot_layout.addWidget(self.canvas)

        # -----------------------------------
        # Add both panels to the splitter.
        # -----------------------------------
        self.splitter.addWidget(self.options_widget)
        self.splitter.addWidget(self.plot_widget)
        self.splitter.setSizes([300, 900])  # Adjust initial sizes as needed.
        self.setCentralWidget(self.splitter)

        # Initialize dataset variables.
        self.datasets = []  # This will be a list of dataset tuples.
        self.selected_dataset = None  # Here, we assign the entire list.

    def on_load_datasets(self):
        """
        Use the text box values for directory and dataset_filter to load datasets.
        """
        directory = self.directory_input.text().strip()
        dataset_filter = self.dataset_filter_input.text().strip() or None

        if not directory:
            QMessageBox.warning(self, "Input Error", "Please enter a valid directory or file path.")
            return

        try:
            self.datasets = load_datasets(directory, dataset_filter=dataset_filter)
            if not self.datasets:
                QMessageBox.warning(self, "No Datasets", "No valid NetCDF datasets were found.")
                return
            # Assign the entire list of loaded datasets.
            self.selected_dataset = self.datasets
            QMessageBox.information(self, "Datasets Loaded", f"Loaded {len(self.datasets)} dataset(s).")
            self.populate_combo_boxes()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load datasets:\n{e}")

    def populate_combo_boxes(self):
        """
        Populate the parameter combo boxes using the list functions,
        with self.selected_dataset passed as the argument.
        """
        if self.selected_dataset is None:
            return

        valid_vars = var_list(self.selected_dataset)
        valid_times = time_list(self.selected_dataset)
        valid_lats = lat_list(self.selected_dataset)
        valid_lons = lon_list(self.selected_dataset)
        valid_levels = level_list(self.selected_dataset)

        self.var_combo.clear()
        self.var_combo.addItems([str(var) for var in valid_vars])
        self.time_combo.clear()
        self.time_combo.addItems([str(t) for t in valid_times])
        self.lat_combo.clear()
        self.lat_combo.addItems([str(lat) for lat in valid_lats])
        self.lon_combo.clear()
        self.lon_combo.addItems([str(lon) for lon in valid_lons])
        if valid_levels:
            self.level_min_input.setText(str(min(valid_levels)))
            self.level_max_input.setText(str(max(valid_levels)))

    def on_plot(self):
        """
        Retrieve parameter values from the UI, call the plotting function,
        and display the resulting plot.
        """
        if self.selected_dataset is None:
            QMessageBox.warning(self, "Dataset Error", "Please load a dataset first.")
            return

        variable_name = self.var_combo.currentText()
        time_val = self.time_combo.currentText()
        try:
            latitude = float(self.lat_combo.currentText())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid latitude value.")
            return

        try:
            longitude = float(self.lon_combo.currentText())
        except ValueError:
            longitude = None

        variable_unit = self.unit_input.text().strip() or None

        level_min_text = self.level_min_input.text().strip()
        try:
            level_minimum = float(level_min_text) if level_min_text else None
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Level Minimum must be a valid number.")
            return

        level_max_text = self.level_max_input.text().strip()
        try:
            level_maximum = float(level_max_text) if level_max_text else None
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Level Maximum must be a valid number.")
            return

        log_level = self.log_level_checkbox.isChecked()
        clean_plot = self.clean_plot_checkbox.isChecked()
        verbose = self.verbose_checkbox.isChecked()

        # Call your plotting function with the selected parameters.
        fig = plt_lev_var(
            self.selected_dataset, variable_name, latitude,
            time=time_val, longitude=longitude,
            log_level=log_level, variable_unit=variable_unit,
            level_minimum=level_minimum, level_maximum=level_maximum,
            clean_plot=clean_plot, verbose=verbose
        )

        # Replace the old canvas with the new plot.
        self.plot_layout.removeWidget(self.canvas)
        self.canvas.deleteLater()
        self.canvas = FigureCanvas(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plot_layout.addWidget(self.canvas)
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

# --- Main entry point ---
if __name__ == '__main__':
    main()
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")  # Use the Qt5Agg backend for PyQt5
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
    QFormLayout, QCheckBox, QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import xarray as xr
from datetime import datetime
from ..plot_gen import plt_lev_var
from ..io import load_datasets, save_output
from ..data_parse import time_list, var_list, level_list, lon_list, lat_list


# ============================================================================
# Main GUI Window
# ============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Level vs Variable Plotter")
        self.setGeometry(100, 100, 1000, 800)
        
        # This will store the list of loaded datasets (each is a tuple: [dataset, file_name, model])
        self.datasets = []
        # We'll use the first dataset (if available) to populate valid parameter lists.
        self.selected_dataset = None
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        
        # Create a form layout for dataset selection and input parameters
        form_layout = QFormLayout()
        
        # Two text boxes for directory and dataset_filter instead of a combo box
        self.directory_input = QLineEdit()
        self.directory_input.setPlaceholderText("Enter directory path or file path")
        form_layout.addRow("Directory:", self.directory_input)
        
        self.dataset_filter_input = QLineEdit()
        self.dataset_filter_input.setPlaceholderText("Optional filter (e.g., 'prim', 'sech')")
        form_layout.addRow("Dataset Filter:", self.dataset_filter_input)
        
        # Use QComboBox for parameters with valid lists (populated from the loaded dataset)
        self.var_combo = QComboBox()
        form_layout.addRow("Variable Name:", self.var_combo)
        
        self.time_combo = QComboBox()
        form_layout.addRow("Time (ISO):", self.time_combo)
        
        self.lat_combo = QComboBox()
        form_layout.addRow("Latitude:", self.lat_combo)
        
        self.lon_combo = QComboBox()
        form_layout.addRow("Longitude:", self.lon_combo)
        
        # Use QLineEdit for parameters without a predefined list
        self.mtime_input = QLineEdit()
        self.mtime_input.setPlaceholderText("e.g., 1,12,0,0")
        form_layout.addRow("mtime (day,hour,min,sec):", self.mtime_input)
        
        self.unit_input = QLineEdit()
        form_layout.addRow("Variable Unit:", self.unit_input)
        
        self.level_min_input = QLineEdit()
        form_layout.addRow("Level Minimum:", self.level_min_input)
        
        self.level_max_input = QLineEdit()
        form_layout.addRow("Level Maximum:", self.level_max_input)
        
        # Boolean options using checkboxes
        self.log_level_checkbox = QCheckBox()
        self.log_level_checkbox.setChecked(True)
        form_layout.addRow("Log Level:", self.log_level_checkbox)
        
        self.clean_plot_checkbox = QCheckBox()
        form_layout.addRow("Clean Plot:", self.clean_plot_checkbox)
        
        self.verbose_checkbox = QCheckBox()
        form_layout.addRow("Verbose:", self.verbose_checkbox)
        
        self.main_layout.addLayout(form_layout)
        
        # Buttons for loading datasets, refreshing lists, and plotting
        btn_layout = QHBoxLayout()
        self.load_button = QPushButton("Load Datasets")
        self.load_button.clicked.connect(self.on_load_datasets)
        btn_layout.addWidget(self.load_button)
        
        self.refresh_button = QPushButton("Refresh Valid Lists")
        self.refresh_button.clicked.connect(self.populate_combo_boxes)
        btn_layout.addWidget(self.refresh_button)
        
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.on_plot)
        btn_layout.addWidget(self.plot_button)
        
        self.main_layout.addLayout(btn_layout)
        
        # Matplotlib canvas to display the plot
        self.canvas = FigureCanvas(plt.figure(figsize=(10, 6)))
        self.main_layout.addWidget(self.canvas)
    
    def on_load_datasets(self):
        """
        Use the values from the two text boxes (directory and dataset_filter) to load datasets.
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
            # Use the first dataset from the loaded list to populate the valid lists.
            self.selected_dataset = self.datasets
            QMessageBox.information(self, "Datasets Loaded", f"Loaded {len(self.datasets)} dataset(s).")
            self.populate_combo_boxes()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load datasets:\n{e}")
    
    def populate_combo_boxes(self):
        """
        Populate the parameter combo boxes with valid lists from your helper functions,
        using the selected dataset.
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
        
        # Optionally, set default level min/max values based on the valid levels
        if valid_levels:
            self.level_min_input.setText(str(min(valid_levels)))
            self.level_max_input.setText(str(max(valid_levels)))
    
    def on_plot(self):
        """
        Retrieve all parameter values from the GUI, call the plotting function,
        and display the resulting figure in the embedded matplotlib canvas.
        """
        if self.selected_dataset is None:
            QMessageBox.warning(self, "Dataset Error", "Please load a dataset first.")
            return
        
        # Retrieve parameters from combo boxes and text inputs
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
        
        mtime_text = self.mtime_input.text().strip()
        if mtime_text:
            try:
                mtime = [int(s.strip()) for s in mtime_text.split(",")]
            except ValueError:
                QMessageBox.warning(self, "Input Error", "mtime must be comma-separated integers.")
                return
        else:
            mtime = None
        
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
        
        # Call your plotting function with the selected parameters
        fig = plt_lev_var(
            self.selected_dataset, variable_name, latitude,
            time=time_val, mtime=mtime, longitude=longitude,
            log_level=log_level, variable_unit=variable_unit,
            level_minimum=level_minimum, level_maximum=level_maximum,
            clean_plot=clean_plot, verbose=verbose
        )
        
        # Replace the old canvas with the new plot
        self.main_layout.removeWidget(self.canvas)
        self.canvas.deleteLater()
        self.canvas = FigureCanvas(fig)
        self.main_layout.addWidget(self.canvas)
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

# --- Main entry point ---
if __name__ == '__main__':
    main()
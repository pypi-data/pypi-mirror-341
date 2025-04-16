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
    QComboBox, QMessageBox, QFileDialog, QLabel, QSizePolicy, QStackedWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import xarray as xr
from datetime import datetime
from ..plot_gen import plt_lev_var, plt_lat_lon, plt_lev_lat, plt_lev_lon, plt_lev_time, plt_lat_time
from ..io import load_datasets, save_output
from ..data_parse import time_list, var_list, level_list, lon_list, lat_list



# ----------------------------------------------------------------------------
# Main GUI – organized into Dataset, Plot Type, and Plot Parameters sections.
# ----------------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Plot GUI")
        self.resize(1200, 600)
        
        # Main splitter divides window into left (controls) and right (plot)
        self.splitter = QSplitter(Qt.Horizontal)
        
        # --- Left Panel: Controls ---
        self.controls_widget = QWidget()
        self.controls_layout = QVBoxLayout(self.controls_widget)
        
        # Dataset Group
        self.dataset_group = QGroupBox("Dataset")
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
        self.controls_layout.addWidget(self.dataset_group)
        
        # Plot Type Group
        self.plot_type_group = QGroupBox("Plot Type")
        pt_layout = QHBoxLayout()
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems([
            "Lat vs Lon", 
            "Lev vs Var", 
            "Lev vs Lon", 
            "Lev vs Lat", 
            "Lev vs Time", 
            "Lat vs Time"
        ])
        self.plot_type_combo.currentIndexChanged.connect(self.on_plot_type_changed)
        pt_layout.addWidget(self.plot_type_combo)
        self.plot_type_group.setLayout(pt_layout)
        self.controls_layout.addWidget(self.plot_type_group)
        
        # Plot Parameters Group – use a QStackedWidget so parameters change with plot type
        self.param_stack = QStackedWidget()
        # Page for "Lat vs Lon" (using plt_lat_lon)
        self.page_lat_lon = self.create_lat_lon_page()
        # Page for "Lev vs Var" (using plt_lev_var)
        self.page_lev_var = self.create_lev_var_page()
        # For other plot types, add placeholder pages
        self.page_lev_lon = self.create_placeholder_page("Lev vs Lon Parameters (to be implemented)")
        self.page_lev_lat = self.create_placeholder_page("Lev vs Lat Parameters (to be implemented)")
        self.page_lev_time = self.create_placeholder_page("Lev vs Time Parameters (to be implemented)")
        self.page_lat_time = self.create_placeholder_page("Lat vs Time Parameters (to be implemented)")
        
        self.param_stack.addWidget(self.page_lat_lon)   # index 0
        self.param_stack.addWidget(self.page_lev_var)     # index 1
        self.param_stack.addWidget(self.page_lev_lon)     # index 2
        self.param_stack.addWidget(self.page_lev_lat)     # index 3
        self.param_stack.addWidget(self.page_lev_time)    # index 4
        self.param_stack.addWidget(self.page_lat_time)    # index 5
        
        self.controls_layout.addWidget(self.param_stack)
        
        # Plot Button
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.on_plot)
        self.controls_layout.addWidget(self.plot_button)
        
        self.controls_layout.addStretch()
        
        # --- Right Panel: Plot Display ---
        self.plot_widget = QWidget()
        self.plot_layout = QVBoxLayout(self.plot_widget)
        self.canvas = FigureCanvas(plt.figure(figsize=(10,6)))
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plot_layout.addWidget(self.canvas)
        
        # Add panels to splitter
        self.splitter.addWidget(self.controls_widget)
        self.splitter.addWidget(self.plot_widget)
        self.splitter.setSizes([300, 900])
        self.setCentralWidget(self.splitter)
        
        # Dataset storage
        self.datasets = []  # list of dataset tuples
        self.selected_dataset = None  # will store the entire list
        
    # --- Parameter Pages ---
    def create_lat_lon_page(self):
        """Create parameters for plt_lat_lon."""
        page = QWidget()
        layout = QFormLayout(page)
        self.ll_variable_combo = QComboBox()
        layout.addRow("Variable Name:", self.ll_variable_combo)
        self.ll_time_combo = QComboBox()
        layout.addRow("Time (ISO):", self.ll_time_combo)
        self.ll_level_combo = QComboBox()
        layout.addRow("Level:", self.ll_level_combo)
        self.ll_unit_input = QLineEdit()
        layout.addRow("Variable Unit:", self.ll_unit_input)
        self.ll_center_lon_input = QLineEdit()
        self.ll_center_lon_input.setText("0")
        layout.addRow("Center Longitude:", self.ll_center_lon_input)
        self.ll_contour_intervals_input = QLineEdit()
        self.ll_contour_intervals_input.setText("20")
        layout.addRow("Contour Intervals:", self.ll_contour_intervals_input)
        self.ll_contour_value_input = QLineEdit()
        layout.addRow("Contour Value:", self.ll_contour_value_input)
        self.ll_symmetric_checkbox = QCheckBox()
        layout.addRow("Symmetric Interval:", self.ll_symmetric_checkbox)
        self.ll_cmap_input = QLineEdit()
        layout.addRow("Colormap:", self.ll_cmap_input)
        self.ll_cmap_lim_min_input = QLineEdit()
        layout.addRow("Colormap Min:", self.ll_cmap_lim_min_input)
        self.ll_cmap_lim_max_input = QLineEdit()
        layout.addRow("Colormap Max:", self.ll_cmap_lim_max_input)
        self.ll_line_color_input = QLineEdit()
        self.ll_line_color_input.setText("white")
        layout.addRow("Line Color:", self.ll_line_color_input)
        self.ll_coastlines_checkbox = QCheckBox()
        layout.addRow("Coastlines:", self.ll_coastlines_checkbox)
        self.ll_nightshade_checkbox = QCheckBox()
        layout.addRow("Nightshade:", self.ll_nightshade_checkbox)
        self.ll_gm_equator_checkbox = QCheckBox()
        layout.addRow("GM Equator:", self.ll_gm_equator_checkbox)
        self.ll_lat_min_input = QLineEdit()
        layout.addRow("Latitude Min:", self.ll_lat_min_input)
        self.ll_lat_max_input = QLineEdit()
        layout.addRow("Latitude Max:", self.ll_lat_max_input)
        self.ll_lon_min_input = QLineEdit()
        layout.addRow("Longitude Min:", self.ll_lon_min_input)
        self.ll_lon_max_input = QLineEdit()
        layout.addRow("Longitude Max:", self.ll_lon_max_input)
        self.ll_clean_checkbox = QCheckBox()
        layout.addRow("Clean Plot:", self.ll_clean_checkbox)
        self.ll_verbose_checkbox = QCheckBox()
        layout.addRow("Verbose:", self.ll_verbose_checkbox)
        return page
        
    def create_lev_var_page(self):
        """Create parameters for plt_lev_var."""
        page = QWidget()
        layout = QFormLayout(page)
        self.lv_variable_combo = QComboBox()
        layout.addRow("Variable Name:", self.lv_variable_combo)
        self.lv_lat_combo = QComboBox()
        layout.addRow("Latitude:", self.lv_lat_combo)
        self.lv_time_combo = QComboBox()
        layout.addRow("Time (ISO):", self.lv_time_combo)
        self.lv_lon_combo = QComboBox()
        layout.addRow("Longitude:", self.lv_lon_combo)
        self.lv_unit_input = QLineEdit()
        layout.addRow("Variable Unit:", self.lv_unit_input)
        self.lv_level_min_input = QLineEdit()
        layout.addRow("Level Min:", self.lv_level_min_input)
        self.lv_level_max_input = QLineEdit()
        layout.addRow("Level Max:", self.lv_level_max_input)
        self.lv_log_checkbox = QCheckBox()
        self.lv_log_checkbox.setChecked(True)
        layout.addRow("Log Level:", self.lv_log_checkbox)
        self.lv_clean_checkbox = QCheckBox()
        layout.addRow("Clean Plot:", self.lv_clean_checkbox)
        self.lv_verbose_checkbox = QCheckBox()
        layout.addRow("Verbose:", self.lv_verbose_checkbox)
        return page
        
    def create_placeholder_page(self, text):
        """Create a placeholder page for unimplemented plot types."""
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(text)
        layout.addWidget(label)
        layout.addStretch()
        return page
        
    # --- Slots ---
    def on_plot_type_changed(self, index):
        self.param_stack.setCurrentIndex(index)
        
    def on_load_datasets(self):
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
            # Assign the entire list
            self.selected_dataset = self.datasets
            QMessageBox.information(self, "Datasets Loaded", f"Loaded {len(self.datasets)} dataset(s).")
            self.populate_common_lists()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load datasets:\n{e}")
            
    def populate_common_lists(self):
        # Use the list functions with self.selected_dataset
        valid_vars = var_list(self.selected_dataset)
        valid_times = time_list(self.selected_dataset)
        valid_lats = lat_list(self.selected_dataset)
        valid_lons = lon_list(self.selected_dataset)
        valid_levels = level_list(self.selected_dataset)
        
        # Populate fields in Lat vs Lon page
        self.ll_variable_combo.clear()
        self.ll_variable_combo.addItems([str(v) for v in valid_vars])
        self.ll_time_combo.clear()
        self.ll_time_combo.addItems([str(t) for t in valid_times])
        self.ll_level_combo.clear()
        self.ll_level_combo.addItems([str(lev) for lev in valid_levels])

        # Populate fields in Lev vs Var page
        self.lv_variable_combo.clear()
        self.lv_variable_combo.addItems([str(v) for v in valid_vars])
        self.lv_lat_combo.clear()
        self.lv_lat_combo.addItems([str(lat) for lat in valid_lats])
        self.lv_time_combo.clear()
        self.lv_time_combo.addItems([str(t) for t in valid_times])
        self.lv_lon_combo.clear()
        self.lv_lon_combo.addItems([str(lon) for lon in valid_lons])
        
        
    def on_plot(self):
        plot_type = self.plot_type_combo.currentText()
        fig = None
        print("in")
        if plot_type == "Lat vs Lon":
            params = {
                "datasets": self.selected_dataset,
                "variable_name": self.ll_variable_combo.currentText(),
                "time": self.ll_time_combo.currentText(),
                "level": self.ll_level_combo.currentText(),
                "variable_unit": self.ll_unit_input.text(),
                "center_longitude": float(self.ll_center_lon_input.text()) if self.ll_center_lon_input.text() else 0,
                "contour_intervals": int(self.ll_contour_intervals_input.text()) if self.ll_contour_intervals_input.text() else 20,
                "contour_value": int(self.ll_contour_value_input.text()) if self.ll_contour_value_input.text() else None,
                "symmetric_interval": self.ll_symmetric_checkbox.isChecked(),
                "cmap_color": self.ll_cmap_input.text() or None,
                "cmap_lim_min": float(self.ll_cmap_lim_min_input.text()) if self.ll_cmap_lim_min_input.text() else None,
                "cmap_lim_max": float(self.ll_cmap_lim_max_input.text()) if self.ll_cmap_lim_max_input.text() else None,
                "line_color": self.ll_line_color_input.text() or None,
                "coastlines": self.ll_coastlines_checkbox.isChecked(),
                "nightshade": self.ll_nightshade_checkbox.isChecked(),
                "gm_equator": self.ll_gm_equator_checkbox.isChecked(),
                "latitude_minimum": float(self.ll_lat_min_input.text()) if self.ll_lat_min_input.text() else None,
                "latitude_maximum": float(self.ll_lat_max_input.text()) if self.ll_lat_max_input.text() else None,
                "longitude_minimum": float(self.ll_lon_min_input.text()) if self.ll_lon_min_input.text() else None,
                "longitude_maximum": float(self.ll_lon_max_input.text()) if self.ll_lon_max_input.text() else None,
                "clean_plot": self.ll_clean_checkbox.isChecked(),
                "verbose": self.ll_verbose_checkbox.isChecked()
            }
            print(params)
            fig = plt_lat_lon(**params)
        elif plot_type == "Lev vs Var":
            params = {
                "datasets": self.selected_dataset,
                "variable_name": self.lv_variable_combo.currentText(),
                "latitude": float(self.lv_lat_combo.currentText()) if self.lv_lat_combo.currentText() else None,
                "time": self.lv_time_combo.currentText(),
                "longitude": float(self.lv_lon_combo.currentText()) if self.lv_lon_combo.currentText() else None,
                "log_level": self.lv_log_checkbox.isChecked(),
                "variable_unit": self.lv_unit_input.text() or None,
                "level_minimum": float(self.lv_level_min_input.text()) if self.lv_level_min_input.text() else None,
                "level_maximum": float(self.lv_level_max_input.text()) if self.lv_level_max_input.text() else None,
                "clean_plot": self.lv_clean_checkbox.isChecked(),
                "verbose": self.lv_verbose_checkbox.isChecked()
            }
            fig = plt_lev_var(**params)
        elif plot_type == "Lev vs Lon":
            QMessageBox.information(self, "Info", "Lev vs Lon plotting not implemented yet.")
            return
        elif plot_type == "Lev vs Lat":
            QMessageBox.information(self, "Info", "Lev vs Lat plotting not implemented yet.")
            return
        elif plot_type == "Lev vs Time":
            QMessageBox.information(self, "Info", "Lev vs Time plotting not implemented yet.")
            return
        elif plot_type == "Lat vs Time":
            QMessageBox.information(self, "Info", "Lat vs Time plotting not implemented yet.")
            return
        else:
            QMessageBox.warning(self, "Plot Type Error", "Unknown plot type selected.")
            return
        
        # Update the canvas with the new figure.
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
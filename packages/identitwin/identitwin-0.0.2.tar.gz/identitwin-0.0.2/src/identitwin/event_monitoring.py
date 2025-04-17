"""
Event monitoring module for the IdentiTwin system.

This module provides real-time monitoring and detection of structural events based on:
- Acceleration thresholds
- Displacement thresholds
- Event duration analysis

Key Features:
- Continuous sensor data monitoring
- Pre-trigger and post-trigger data buffering
- Event data persistence and analysis
- Multi-threaded event processing
- Moving average filtering for noise reduction
- Adaptive trigger/detrigger mechanism

Classes:
    EventMonitor: Main class for event detection and handling

The module integrates with the data processing and analysis modules for complete
event lifecycle management from detection to analysis and storage.
"""

import os
import csv
import time
import queue
import traceback
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import logging
from collections import deque
from datetime import datetime

from . import state
from .processing_data import read_lvdt_data
from . import processing_analysis

# event_monitoring.py
class EventMonitor:
    """Monitors events based on sensor data and saves relevant information."""

    def __init__(self, config, data_queue, thresholds, running_ref, event_count_ref):
        """
        Initializes the EventMonitor.

        Args:
            config: The system configuration object.
            data_queue: A queue containing sensor data.
            thresholds: A dictionary of thresholds for event detection.
            running_ref: A reference to a boolean indicating whether the system is running.
            event_count_ref: A reference to an integer tracking the number of events.

        Returns:
            None

        Assumptions:
            - The configuration object is properly set up.
            - The data queue provides sensor data in a consistent format.
            - Thresholds for acceleration and displacement are provided.
            - The running_ref is a shared boolean to control the thread.
            - The event_count_ref is a shared counter for events.
        """
        self.config = config
        self.data_queue = data_queue
        self.thresholds = thresholds
        self.running_ref = running_ref
        self.event_count_ref = event_count_ref
        self.event_in_progress = False
        self.event_data_buffer = queue.Queue(maxsize=1000)
        
        self.in_event_recording = False
        self.current_event_data = []
        self.pre_trigger_buffer = deque(maxlen=1000)  # adjust buffer size as needed
        self.last_trigger_time = 0
        
        # Initialize moving averages with deque buffers
        window_size = int(0.5 * config.sampling_rate_acceleration)  # 0.5 segundos de muestras
        self.accel_buffer = deque(maxlen=200)
        self.disp_buffer = deque(maxlen=10)
        self.moving_avg_accel = 0.0
        self.moving_avg_disp = 0.0

        # Initialize event count in state with current value
        state.set_event_variable("event_count", event_count_ref[0])
        state.set_event_variable("is_event_recording", False)
        
        self.error_count = 0
        self.max_errors = 100  # Maximum number of consecutive errors before warning

    def detect_event(self, sensor_data):
        """Detect and record event data using trigger/detrigger mechanism."""
        if not sensor_data or "sensor_data" not in sensor_data:
            return False
        
        try:
            self.pre_trigger_buffer.append(sensor_data)
            current_time = time.time()
            
            # Extract and validate sensor data
            accel_data = sensor_data.get("sensor_data", {}).get("accel_data", [])
            lvdt_data = sensor_data.get("sensor_data", {}).get("lvdt_data", [])
            
            if not accel_data and not lvdt_data:
                return False

            # Process sensor data safely
            magnitude = 0
            instantaneous_disp = 0

            if accel_data and len(accel_data) > 0:
                accel = accel_data[0]
                if all(k in accel for k in ['x', 'y', 'z']):
                    magnitude = np.sqrt(accel["x"]**2 + accel["y"]**2 + accel["z"]**2)
                    self.accel_buffer.append(magnitude)
                    self.moving_avg_accel = np.mean(self.accel_buffer)

            if lvdt_data and len(lvdt_data) > 0:
                instantaneous_disp = abs(lvdt_data[0].get("displacement", 0))
                self.disp_buffer.append(instantaneous_disp)
                self.moving_avg_disp = np.mean(self.disp_buffer)

            # Event detection logic
            trigger_accel = self.thresholds.get("acceleration", 0.981)
            trigger_disp = self.thresholds.get("displacement", 2.0)
            
            accel_trigger = magnitude > trigger_accel
            lvdt_trigger = instantaneous_disp > trigger_disp

            if accel_trigger or lvdt_trigger:
                return self._handle_event_trigger(sensor_data, current_time, magnitude, instantaneous_disp)
            elif self.in_event_recording:
                return self._handle_event_recording(sensor_data, current_time)
                
            return True

        except Exception as e:
            self.error_count += 1
            if self.error_count >= self.max_errors:
                logging.error(f"Multiple errors in event detection: {e}")
                self.error_count = 0
            return False

    def _handle_event_trigger(self, sensor_data, current_time, magnitude, displacement):
        """Handle event trigger logic"""
        try:
            self.last_trigger_time = current_time
            
            if not self.in_event_recording:
                print(f"\n*** NEW EVENT DETECTED at {sensor_data['timestamp']} ***")
                self.in_event_recording = True
                state.set_event_variable("is_event_recording", True)
                state.set_event_variable("last_trigger_time", current_time)
                self.current_event_data = list(self.pre_trigger_buffer)
            
            self.current_event_data.append(sensor_data)
            return True
            
        except Exception as e:
            logging.error(f"Error in event trigger handling: {e}")
            return False

    def _handle_event_recording(self, sensor_data, current_time):
        """Handle ongoing event recording and check for completion"""
        try:
            self.current_event_data.append(sensor_data)
            post_trigger_time = self.thresholds.get("post_event_time", 15.0)
            
            if current_time - self.last_trigger_time > post_trigger_time:
                event_duration = len(self.current_event_data) * self.config.time_step_acceleration
                min_duration = self.thresholds.get("min_event_duration", 2.0)
                
                if event_duration >= min_duration:
                    try:
                        self.event_data_buffer.put(self.current_event_data)
                        self.event_count_ref[0] += 1
                        event_time = self.current_event_data[0]["timestamp"]
                        self._save_event_data(self.current_event_data, event_time)
                        print(f"Event complete - duration={event_duration:.2f}s")
                    except Exception as e:
                        logging.error(f"Error saving event: {e}")
                
                # Reset event state
                self.in_event_recording = False
                self.current_event_data = []
                self.pre_trigger_buffer.clear()
                state.set_event_variable("is_event_recording", False)
            
            return True
            
        except Exception as e:
            logging.error(f"Error in event recording handling: {e}")
            return False

    def event_monitoring_thread(self):
        """Thread function for monitoring events."""
        while self.running_ref:
            try:
                if not self.data_queue:
                    time.sleep(0.001)
                    continue
                    
                sensor_data = self.data_queue.popleft()
                if not self.detect_event(sensor_data):
                    continue
                    
            except Exception as e:
                logging.error(f"Error in monitoring thread: {e}")
                time.sleep(0.1)  # Prevent tight error loop
                
        self._cleanup_on_exit()

    def _cleanup_on_exit(self):
        """Clean up resources when thread exits"""
        try:
            if self.in_event_recording and self.current_event_data:
                self._finalize_event()
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

    def _save_event_data(self, event_data, start_time):
        """Save event data to CSV file and generate plots."""
        try:
            # Initialize tracking variables
            seen_timestamps = set()
            processed_data = []
            sample_count = 0
            
            # Process each data point
            for data in event_data:
                if 'timestamp' not in data:
                    continue
                    
                if data['timestamp'] not in seen_timestamps:
                    seen_timestamps.add(data['timestamp'])
                    
                    # Add expected time based on sample number
                    expected_time = sample_count * (1.0 / self.config.sampling_rate_acceleration)
                    data['expected_time'] = expected_time
                    processed_data.append(data)
                    sample_count += 1

            if not processed_data:
                logging.error("No valid data to save")
                return False

            # Save processed data
            report_file = processing_analysis.save_event_data(
                event_data=processed_data,
                start_time=start_time,
                config=self.config
            )

            if report_file:
                current_count = self.event_count_ref[0]
                state.set_event_variable("event_count", current_count)
                print(f"Event {current_count} saved successfully to {report_file}")
                return True

            return False

        except Exception as e:
            logging.error(f"Error saving event data: {e}")
            traceback.print_exc()
            return False

    def _generate_plots(self, event_data, event_dir):
        """Generates plots for acceleration and displacement using thread-safe approach."""
        timestamps = []
        accel_magnitudes = []
        displacements = []

        for entry in event_data:
            try:
                timestamps.append(entry["timestamp"])

                accel_magnitude = 0
                if (
                    "sensor_data" in entry
                    and "accel_data" in entry["sensor_data"]
                ):
                    accel = entry["sensor_data"]["accel_data"][0]
                    accel_magnitude = np.sqrt(
                        accel["x"] ** 2 + accel["y"] ** 2 + accel["z"] ** 2
                    )

                displacements_value = 0
                if (
                    "sensor_data" in entry
                    and "lvdt_data" in entry["sensor_data"]
                ):
                    displacements_value = entry["sensor_data"]["lvdt_data"][0]["displacement"]

                accel_magnitudes.append(accel_magnitude)
                displacements.append(displacements_value)

            except KeyError as e:
                logging.error(f"Missing key in event data: {e}")
                continue
            except Exception as e:
                logging.error(f"Error processing data for plotting: {e}")
                continue

        # Check if we have any data to plot
        if not timestamps or not accel_magnitudes or not displacements:
            logging.warning("No data to generate plots.")
            return

        try:
            # Calculate expected timestamps based on acceleration rate
            sample_count = len(timestamps)
            relative_timestamps = [i * self.config.time_step_acceleration for i in range(sample_count)]

            # Use a thread-safe approach without pyplot
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
            
            # Create acceleration plot
            fig = Figure(figsize=(10, 6))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.plot(relative_timestamps, accel_magnitudes)
            ax.set_title("Acceleration Magnitude vs Time")
            ax.set_xlabel("Time (seconds)")
            ax.set_ylabel("Acceleration (m/s2)")
            ax.grid(True)
            fig.tight_layout()
            fig.savefig(os.path.join(event_dir, "acceleration_plot.png"))
            
            # Create displacement plot with a new figure
            fig = Figure(figsize=(10, 6))
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.plot(relative_timestamps, displacements)
            ax.set_title("Displacement vs Time")
            ax.set_xlabel("Time (seconds)")
            ax.set_ylabel("Displacement (mm)")
            ax.grid(True)
            fig.tight_layout()
            fig.savefig(os.path.join(event_dir, "displacement_plot.png"))

        except Exception as e:
            logging.error(f"Error generating plots: {e}")
            traceback.print_exc()

    def _finalize_event(self):
        """Helper method to finalize and save event data."""
        try:
            event_time = self.current_event_data[0]["timestamp"]
            if self._save_event_data(self.current_event_data, event_time):
                # Only increment counter if event was successfully saved
                self.event_count_ref[0] += 1
                state.set_event_variable("event_count", self.event_count_ref[0])
                print(f"Event {self.event_count_ref[0]} successfully recorded and saved")
        except Exception as e:
            print(f"Error saving event: {e}")
        
        # Reset all event state
        self.in_event_recording = False
        self.current_event_data = []
        self.pre_trigger_buffer.clear()
        self.last_detrigger_time = 0
        self.min_duration_met = False
        state.set_event_variable("is_event_recording", False)

def print_event_banner():
    """Print a  banner when the event starts"""
    banner = """
===============================================================================
    Event is starting, please wait...
    Event Monitoring System...
===============================================================================
    """
    print(banner)
    time.sleep(2)  # Pause for 2 seconds
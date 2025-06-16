# Protocol_automated_CC

## Overview

`Protocol_automated_CC` is an open-source project for building and operating a high-throughput automated platform for column chromatography. The platform integrates hardware (pumps, autosampler, UV detector, column) and Python-based software to enable fully automated data collection, signal processing, and retention time analysis under multiple experimental conditions.

## Features

- Modular hardware assembly instructions
- Python scripts for device control and workflow automation
- Automated collection and storage of UV chromatographic data
- Signal conversion, baseline correction, peak identification, and retention time calculation
- Export of processed data for downstream analysis

## Repository Structure

- `design_scheme/`  
  Hardware design files and assembly guides
- `Controlling_code/`  
  Python scripts for instrument control and data processing

## Getting Started

1. Assemble the hardware platform following the guides in `design_scheme/`.
2. Connect all devices to the computer via serial ports.
3. Install Python 3.7+ and required packages (`numpy`, `pandas`, `tkinter`, etc.).
4. Run the control scripts in `Controlling_code/` to start automated experiments.
5. Collected data and analysis results will be saved automatically.

## Data Processing

- Raw UV signals are converted to absorbance values using custom algorithms.
- Peaks are detected and retention times are calculated automatically.
- Results are exported in CSV/Excel format for further analysis.

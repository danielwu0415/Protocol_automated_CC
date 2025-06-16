## Overview

`Auto_run.py` is a Python script designed for automated control and data acquisition in a high-throughput column chromatography platform. It integrates hardware control (pumps, autosampler, UV detector) and provides a graphical user interface (GUI) for easy operation. The script enables automated collection of UV chromatographic data, signal conversion, peak identification, and retention time analysis.

## Features

- Serial communication with pumps, autosampler, and UV detector
- Automated execution of multi-condition chromatography runs
- Real-time data acquisition and storage in CSV/Excel format
- Signal conversion from raw hexadecimal to absorbance values
- Automated peak detection and retention time calculation
- User-friendly GUI for parameter input and device control

## Requirements

- Python 3.7 or above
- Required packages: `tkinter`, `numpy`, `pandas`, `datetime`, `threading`
- Compatible hardware: pumps, autosampler, UV detector with serial interface

## Usage

1. Connect all hardware devices to the computer via serial ports.
2. Install required Python packages if not already installed.
3. Run the script:
    ```
    python Auto_run.py
    ```
4. Use the GUI to set parameters and start automated runs.
5. Collected data and analysis results will be saved automatically.

## Data Processing

- Raw UV signals are read as hexadecimal strings via serial port.
- Signals are converted to absorbance using a custom algorithm.
- Peaks are identified, and retention times are calculated automatically.
- Results are exported for further analysis.

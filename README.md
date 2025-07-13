# Event Monitoring

This project implements an event processing pipeline from a log file, generates alerts, produces visual statistics and a PDF report, and provides a basic user interface.

> Link to the [presentation video](https://www.loom.com/share/4991544e43634906928f92d850d9d1c1?sid=3389e641-1faa-4024-b856-17f9555b93da).
---

## Project Structure

Here is the project structure:
```
event_monitoring/
├── input/                   # Input folder
│   └── events.log          # Log file to be processed
├── outputs/                 # Output folder
│   ├── alerts.json         # Detected alerts in JSON format
│   ├── stats.png           # Graphical statistics (histogram)
│   └── report.pdf          # Generated PDF report
├── src/                     # Source code folder
│   ├── main.py             # Entry point of the application
│   ├── fonts/              
│   │   └── NotoEmoji-Regular.ttf  # Font for emojis in the PDF report
│   ├── models/              # Models for events and alerts
│   │   ├── alert.py      
│   │   ├── event.py      
│   │   ├── event_analyzer.py # Analyzes events and detects anomalies
│   │   └── event_logger.py # Performs logging of events
│   └── utils/              # Utility functions
│       ├── processing.py   # Loading and preprocessing of log lines
│       ├── plot_generation.py # Generates charts (histogram)
│       ├── report_generation.py # Generates PDF report
│       └── ui_interface.py # User interface functions
├── README.md             
└── requirements.txt     
```

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/ciajudith/event_monitoring
   cd event_monitoring
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   # Sous macOS/Linux
   source .venv/bin/activate
   # Sous Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

From the project root and with the virtual environment activated, run the application with the following command:
```bash
python -m src.main
```
---

## Functionalities

1. **Loading and preprocessing** (`utils/processing.py`): parses log lines into `Event` objects.
2. **Event analysis** (`models/event_analyzer.py`): detects anomalies and creates `Alert` objects.
3. **Chart generation** (`utils/plot_generation.py`): produces a histogram chart saved as `stats.png`.
4. **Report generation** (`utils/report_generation.py`): aggregates results and creates a `report.pdf`.
5. **User interface** (`utils/ui_interface.py`): some CLI functions to manually run each step.

---

>***Made by @ciajudith.***

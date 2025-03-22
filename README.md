# IoT Patient Monitoring System

This Python application simulates an IoT-based patient monitoring system for a healthcare environment. It generates and manages patient data, responsible healthcare providers (doctors), and simulates vital signs monitoring.

## Features

- Patient data management (ID, name, surname, date of birth, room number, assigned doctor)
- Healthcare provider data management (ID, name, surname, phone number)
- Vital signs simulation for patients:
  - Blood pressure (systolic/diastolic)
  - Heart rate
  - Body temperature
  - Oxygen saturation
  - Respiratory rate
- Data persistence using CSV files
- Real-time vital signs monitoring simulation
- Data visualization of patient vital signs

## Data Structure

The system maintains three main data types:

1. **Patients**: Basic patient information linked to a responsible doctor
2. **Responsible Persons**: Healthcare providers (doctors) assigned to patients
3. **Vital Signs**: Simulated patient health metrics with timestamps

## How to Use

### Generate Patient Data and Vital Signs

Run the main script to:
1. Generate sample patient and doctor data
2. Display the data in formatted tables
3. Simulate vital signs monitoring for all patients
4. Save all data to CSV files in the "data" directory

```bash
python patient_monitoring.py
```

### Visualize Patient Data

After generating data, you can visualize the vital signs using the visualization script:

```bash
python visualize_data.py
```

This script generates:
- Individual patient vital signs charts
- Comparative charts of all patients for each vital sign
- Saves all plots to the "plots" directory

## Required Packages

- Python 3.6+
- pandas
- matplotlib

Install dependencies:
```bash
pip install pandas matplotlib
```

## Output Files

- `data/patients.csv`: Patient information
- `data/responsible_persons.csv`: Doctor information
- `data/vital_signs.csv`: Simulated vital signs data with timestamps
- `plots/`: Directory containing visualization charts

## Customization

You can modify the scripts to:
- Adjust the number of monitoring iterations
- Change the interval between readings
- Modify the range of normal values for vital signs
- Add additional patients or healthcare providers
- Create new visualization styles

## Potential IoT Applications

In a real IoT implementation, this system could be expanded to:
- Connect to physical sensors (blood pressure monitors, pulse oximeters, etc.)
- Send alerts for abnormal readings
- Visualize data trends over time
- Integrate with hospital information systems
- Support remote patient monitoring 
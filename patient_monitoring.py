import random
import time
import datetime
import csv
import os
import serial
from dataclasses import dataclass
from typing import List, Dict

# Data structures
@dataclass
class ResponsiblePerson:
    id: int
    name: str
    surname: str
    phone_number: str

@dataclass
class Patient:
    id: int
    name: str
    surname: str
    date_of_birth: datetime.date
    room_number: int
    responsible_person: ResponsiblePerson

@dataclass
class VitalSigns:
    patient_id: int
    timestamp: datetime.datetime
    systolic: int  # mmHg
    diastolic: int  # mmHg
    heart_rate: int  # bpm
    temperature: float  # °C
    oxygen_saturation: int  # %
    respiratory_rate: int  # breaths per minute

# Serial SMS Engine to communicate with GSM modem
class SMSEngine:
    def __init__(self):
        self.port = None
        
    def open_port(self, port_name):
        try:
            self.port = serial.Serial(
                port=port_name,
                baudrate=115200,
                timeout=1,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            return True
        except Exception as ex:
            print(f"Error opening port: {ex}")
            return False
    
    def close_port(self):
        if self.port and self.port.is_open:
            self.port.close()
            
    def send_sms(self, phone_number, message):
        if not self.port or not self.port.is_open:
            print("Serial port is not open")
            return False
        
        try:
            # Initialize the modem
            self.port.write(b'AT\r\n')
            time.sleep(0.2)
            
            # Set SMS text mode
            self.port.write(b'AT+CMGF=1\r\n')
            time.sleep(0.2)
            
            # Set GSM character set
            self.port.write(b'AT+CSCS="GSM"\r\n')
            time.sleep(0.2)
            
            # Set the destination phone number
            self.port.write(f'AT+CMGS="{phone_number}"\r\n'.encode())
            time.sleep(0.2)
            
            # Send the message and the Ctrl+Z character (ASCII 26)
            self.port.write(f'{message}\x1A'.encode())
            time.sleep(1)
            
            # Read response
            response = self.port.read(self.port.in_waiting)
            
            if b'OK' in response:
                print(f"SMS sent successfully to {phone_number}")
                return True
            else:
                print(f"Failed to send SMS: {response}")
                return False
                
        except Exception as ex:
            print(f"Error sending SMS: {ex}")
            return False
    
# Create a list of responsible persons (doctors)
responsible_persons = [
    ResponsiblePerson(1, "Driton", "alija", "+38344922805"),
    ResponsiblePerson(2, "Sarah", "Johnson", "+38344922805"),
    ResponsiblePerson(3, "David", "Williams", "+38344922805"),
    ResponsiblePerson(4, "Emily", "Brown", "+38344922805"),
    ResponsiblePerson(5, "Michael", "Jones", "+38344922805"),
]

# Create a list of patients
patients = [
    Patient(1, "Alice", "Garcia", datetime.date(1975, 5, 15), 101, responsible_persons[0]),
    Patient(2, "Bob", "Miller", datetime.date(1982, 8, 22), 102, responsible_persons[1]),
    Patient(3, "Charlie", "Davis", datetime.date(1968, 3, 10), 103, responsible_persons[2]),
    Patient(4, "Diana", "Rodriguez", datetime.date(1990, 11, 28), 201, responsible_persons[0]),
    Patient(5, "Edward", "Martinez", datetime.date(1955, 7, 4), 202, responsible_persons[3]),
    Patient(6, "Fiona", "Anderson", datetime.date(1972, 1, 19), 203, responsible_persons[4]),
    Patient(7, "George", "Thomas", datetime.date(1988, 9, 2), 301, responsible_persons[1]),
    Patient(8, "Helen", "Jackson", datetime.date(1960, 12, 25), 302, responsible_persons[2]),
    Patient(9, "Ian", "White", datetime.date(1995, 4, 8), 303, responsible_persons[3]),
    Patient(10, "Julia", "Harris", datetime.date(1980, 6, 17), 304, responsible_persons[4]),
]

# Function to print patient data
def print_patients():
    print("\n--- Patient List ---")
    print(f"{'ID':3} {'Name':<10} {'Surname':<12} {'Date of Birth':<12} {'Room':5} {'Doctor':<20}")
    print("-" * 70)
    for patient in patients:
        doctor = f"{patient.responsible_person.name} {patient.responsible_person.surname}"
        dob = patient.date_of_birth.strftime("%Y-%m-%d")
        print(f"{patient.id:<3} {patient.name:<10} {patient.surname:<12} {dob:<12} {patient.room_number:<5} {doctor:<20}")

# Function to print responsible person data
def print_responsible_persons():
    print("\n--- Responsible Persons (Doctors) ---")
    print(f"{'ID':3} {'Name':<10} {'Surname':<12} {'Phone Number':<15}")
    print("-" * 45)
    for person in responsible_persons:
        print(f"{person.id:<3} {person.name:<10} {person.surname:<12} {person.phone_number:<15}")

# Function to simulate vital signs
def simulate_vital_signs(patient_id: int) -> VitalSigns:
    # Normal ranges for vital signs
    # Systolic: 90-140 mmHg
    # Diastolic: 60-90 mmHg
    # Heart rate: 60-100 bpm
    # Temperature: 36.1-37.2 °C
    # Oxygen saturation: 95-100 %
    # Respiratory rate: 12-20 breaths per minute
    
    systolic = random.randint(90, 140)
    diastolic = random.randint(60, 90)
    
    # Ensure diastolic is always lower than systolic
    while diastolic >= systolic:
        diastolic = random.randint(60, 90)
    
    heart_rate = random.randint(60, 100)
    temperature = round(random.uniform(36.1, 37.2), 1)
    oxygen_saturation = random.randint(95, 100)
    respiratory_rate = random.randint(12, 20)
    
    return VitalSigns(
        patient_id=patient_id,
        timestamp=datetime.datetime.now(),
        systolic=systolic,
        diastolic=diastolic,
        heart_rate=heart_rate,
        temperature=temperature,
        oxygen_saturation=oxygen_saturation,
        respiratory_rate=respiratory_rate
    )

# Function to simulate blood pressure with potential hypertension
def simulate_blood_pressure(patient_id: int) -> tuple:
    # Generate blood pressure readings with possibility of high values
    # Normal: < 120 / < 80
    # Elevated: 120-129 / < 80
    # Stage 1 Hypertension: 130-139 / 80-89
    # Stage 2 Hypertension: 140-179 / 90-119
    # Hypertensive Crisis: >= 180 / >= 120
    
    # Generate with weighted probabilities for higher readings
    # This increases chance of triggering our alert conditions
    weights = [70, 10, 10, 7, 3]  # Percentages for each range
    blood_pressure_category = random.choices(
        ["normal", "elevated", "stage1", "stage2", "crisis"], 
        weights=weights, 
        k=1
    )[0]
    
    if blood_pressure_category == "normal":
        systolic = random.randint(90, 119)
        diastolic = random.randint(60, 79)
    elif blood_pressure_category == "elevated":
        systolic = random.randint(120, 129)
        diastolic = random.randint(60, 79)
    elif blood_pressure_category == "stage1":
        systolic = random.randint(130, 139)
        diastolic = random.randint(80, 89)
    elif blood_pressure_category == "stage2":
        systolic = random.randint(140, 179)
        diastolic = random.randint(90, 109)
    else:  # crisis
        systolic = random.randint(180, 200)
        diastolic = random.randint(110, 120)
    
    # Ensure diastolic is always lower than systolic
    while diastolic >= systolic:
        diastolic = max(10, diastolic - 10)
    
    return systolic, diastolic

# Function to monitor blood pressure and generate alerts with SMS notifications
def monitor_blood_pressure(duration_minutes=5, interval_seconds=20, com_port=None):
    print("\n--- Blood Pressure Monitoring Alert System ---")
    print("Monitoring started. Press Ctrl+C to stop.")
    print("-" * 70)
    
    # Initialize SMS engine if port is provided
    sms_engine = None
    if com_port:
        sms_engine = SMSEngine()
        if sms_engine.open_port(com_port):
            print(f"Successfully connected to GSM modem on {com_port}")
        else:
            print(f"Failed to connect to GSM modem. SMS notifications will be disabled.")
            sms_engine = None
    
    iteration = 0
    start_time = datetime.datetime.now()
    
    try:
        while (datetime.datetime.now() - start_time).total_seconds() < duration_minutes * 60:
            iteration += 1
            print(f"\nIteration {iteration} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            all_readings = []
            
            for patient in patients:
                systolic, diastolic = simulate_blood_pressure(patient.id)
                all_readings.append((patient, systolic, diastolic))
                
                doctor = patient.responsible_person
                
                # Check for hypertension conditions and send alerts
                if 160 <= systolic <= 179 and 100 <= diastolic <= 109:
                    alert_message = (
                        f"MODERATE HYPERTENSION ALERT\n"
                        f"Patient: {patient.name} {patient.surname} (ID: {patient.id})\n"
                        f"Blood Pressure: {systolic}/{diastolic} mmHg\n"
                        f"Action: See a doctor or GP as soon as possible"
                    )
                    
                    print(f"\n🚨 {alert_message}")
                    print(f"Doctor: {doctor.name} {doctor.surname}")
                    print(f"Contact: {doctor.phone_number}")
                    
                    # Send SMS if SMS engine is available
                    if sms_engine:
                        sms_sent = sms_engine.send_sms(
                            doctor.phone_number, 
                            alert_message
                        )
                        if sms_sent:
                            print("SMS alert sent successfully")
                        else:
                            print("Failed to send SMS alert")
                    
                elif systolic >= 180 and diastolic >= 110:
                    alert_message = (
                        f"HYPERTENSIVE EMERGENCY ALERT\n"
                        f"Patient: {patient.name} {patient.surname} (ID: {patient.id})\n"
                        f"Blood Pressure: {systolic}/{diastolic} mmHg\n"
                        f"Action: Requires immediate medical attention. Go to hospital."
                    )
                    
                    print(f"\n🚑 {alert_message}")
                    print(f"Doctor: {doctor.name} {doctor.surname}")
                    print(f"Contact: {doctor.phone_number}")
                    
                    # Send SMS if SMS engine is available
                    if sms_engine:
                        sms_sent = sms_engine.send_sms(
                            doctor.phone_number, 
                            alert_message
                        )
                        if sms_sent:
                            print("SMS alert sent successfully")
                        else:
                            print("Failed to send SMS alert")
            
            # Print a summary of all readings
            print("\nCurrent readings:")
            print(f"{'Patient ID':5} {'Name':<12} {'BP Reading':<12}")
            print("-" * 35)
            for patient, sys_bp, dia_bp in all_readings:
                print(f"{patient.id:<5} {patient.name + ' ' + patient.surname:<12} {sys_bp}/{dia_bp} mmHg")
            
            # Save the readings to CSV if needed
            # save_bp_readings_to_csv(all_readings)
            
            # Wait for the next interval
            if (datetime.datetime.now() - start_time).total_seconds() < duration_minutes * 60:
                time.sleep(interval_seconds)
                
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    finally:
        # Close the serial port if it was opened
        if sms_engine:
            sms_engine.close_port()
            print("Serial port closed")
    
    print("\nBlood pressure monitoring completed.")

# Save patient data to CSV
def save_patients_to_csv(filename="patients.csv"):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'surname', 'date_of_birth', 'room_number', 'responsible_person_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for patient in patients:
            writer.writerow({
                'id': patient.id,
                'name': patient.name,
                'surname': patient.surname,
                'date_of_birth': patient.date_of_birth.strftime("%Y-%m-%d"),
                'room_number': patient.room_number,
                'responsible_person_id': patient.responsible_person.id
            })
    print(f"Patient data saved to {filename}")

# Save responsible persons data to CSV
def save_responsible_persons_to_csv(filename="responsible_persons.csv"):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'surname', 'phone_number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for person in responsible_persons:
            writer.writerow({
                'id': person.id,
                'name': person.name,
                'surname': person.surname,
                'phone_number': person.phone_number
            })
    print(f"Responsible persons data saved to {filename}")

# Save vital signs to CSV
def save_vital_signs_to_csv(vital_signs_data, filename="vital_signs.csv"):
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['patient_id', 'timestamp', 'systolic', 'diastolic', 'heart_rate', 
                     'temperature', 'oxygen_saturation', 'respiratory_rate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        for vs in vital_signs_data:
            writer.writerow({
                'patient_id': vs.patient_id,
                'timestamp': vs.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'systolic': vs.systolic,
                'diastolic': vs.diastolic,
                'heart_rate': vs.heart_rate,
                'temperature': vs.temperature,
                'oxygen_saturation': vs.oxygen_saturation,
                'respiratory_rate': vs.respiratory_rate
            })
    
    print(f"Vital signs data saved to {filename}")

# Simulate monitoring vital signs for all patients
def monitor_patients(iterations=5, interval=2):
    print("\n--- Patient Vital Signs Monitoring ---")
    print(f"{'Patient ID':5} {'Name':<8} {'Systolic':8} {'Diastolic':9} {'HR':4} {'Temp':5} {'O2%':4} {'RR':3}")
    print("-" * 56)
    
    all_vital_signs = []
    
    for _ in range(iterations):
        iteration_vital_signs = []
        
        for patient in patients:
            vital_signs = simulate_vital_signs(patient.id)
            iteration_vital_signs.append(vital_signs)
            
            print(f"{patient.id:<5} {patient.name:<8} "
                  f"{vital_signs.systolic:<8} {vital_signs.diastolic:<9} "
                  f"{vital_signs.heart_rate:<4} {vital_signs.temperature:<5} "
                  f"{vital_signs.oxygen_saturation:<4} {vital_signs.respiratory_rate:<3}")
        
        all_vital_signs.extend(iteration_vital_signs)
        
        if _ < iterations - 1:  # Don't sleep after the last iteration
            time.sleep(interval)
    
    return all_vital_signs

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Display all patients
    print_patients()
    
    # Display all responsible persons
    print_responsible_persons()
    
    # Specify COM port for GSM modem (change as needed)
    # Examples: 'COM3' on Windows, '/dev/ttyUSB0' on Linux, '/dev/tty.usbserial' on macOS
    gsm_port = 'COM3'  # Change this to your actual COM port
    
    # Save data to CSV files (commented out to avoid overwriting)
    #save_patients_to_csv("data/patients.csv")
    #save_responsible_persons_to_csv("data/responsible_persons.csv")
    
    # Run the blood pressure monitoring system with SMS notifications
    monitor_blood_pressure(duration_minutes=5, interval_seconds=20, com_port=gsm_port)
    
    # Alternatively, to run the original simulation:
    # vital_signs_data = monitor_patients(iterations=3, interval=1)
    # save_vital_signs_to_csv(vital_signs_data, "data/vital_signs.csv") 
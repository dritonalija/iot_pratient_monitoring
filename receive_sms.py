import serial
import time
from patient_monitoring import SMSEngine

def receive_sms(com_port: str = "COM5"):
    """
    Continuously monitor and receive SMS messages.
    
    Args:
        com_port (str): The COM port where the GSM modem is connected
    """
    # Initialize the SMS engine
    sms_engine = SMSEngine()
    
    try:
        # Open the serial port
        if sms_engine.open_port(com_port):
            print(f"Successfully connected to GSM modem on {com_port}")
            print("Waiting for incoming SMS messages...")
            print("Press Ctrl+C to stop")
            
            while True:
                try:
                    # Initialize the modem
                    sms_engine.port.write(b'AT\r\n')
                    time.sleep(0.2)
                    
                    # Set SMS text mode
                    sms_engine.port.write(b'AT+CMGF=1\r\n')
                    time.sleep(0.2)
                    
                    # Set GSM character set
                    sms_engine.port.write(b'AT+CSCS="GSM"\r\n')
                    time.sleep(0.2)
                    
                    # Read unread messages only
                    sms_engine.port.write(b'AT+CMGL="REC UNREAD"\r\n')
                    time.sleep(1)
                    
                    # Read response
                    response = sms_engine.port.read(sms_engine.port.in_waiting)
                    
                    if response:
                        # Convert bytes to string and print
                        message = response.decode('utf-8', errors='ignore')
                        print("\nReceived SMS:")
                        print("-" * 50)
                        print(message)
                        print("-" * 50)
                    
                    # Wait before checking again
                    time.sleep(5)
                    
                except KeyboardInterrupt:
                    print("\nStopping SMS receiver...")
                    break
                    
        else:
            print(f"Failed to connect to GSM modem on {com_port}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Always close the port
        sms_engine.close_port()
        print("Serial port closed")

if __name__ == "__main__":
    # Example usage
    com_port = "COM5"  # Replace with your actual COM port
    
    print("Starting SMS receiver...")
    receive_sms(com_port) 
import serial
import time
from patient_monitoring import SMSEngine

def make_call(phone_number: str, com_port: str = "COM5"):
    """
    Make a call from the device to a specified phone number.
    
    Args:
        phone_number (str): The phone number to call
        com_port (str): The COM port where the GSM modem is connected
    """
    # Initialize the SMS engine
    sms_engine = SMSEngine()
    
    try:
        # Open the serial port
        if sms_engine.open_port(com_port):
            print(f"Successfully connected to GSM modem on {com_port}")
            print(f"Attempting to call {phone_number}...")
            
            # Make the call
            if sms_engine.make_call(phone_number):
                print("Call initiated successfully")
                print("Call is in progress...")
                
                # Wait for user to end the call
                input("Press Enter to end the call...")
                
                # End the call
                if sms_engine.end_call():
                    print("Call ended successfully")
                else:
                    print("Failed to end call")
            else:
                print("Failed to initiate call")
                
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
    phone_number = "+38344922805"  # Replace with your actual phone number
    com_port = "COM5"  # Replace with your actual COM port
    
    print("Starting call maker...")
    make_call(phone_number, com_port) 
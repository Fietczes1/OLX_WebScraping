import platform
import time
from gsmmodem.modem import GsmModem

# Determine the serial port based on the platform
if platform.system() == "Windows":
    port = "COM3"  # Replace with your Windows COM port
else:
    port = "/dev/ttyS0"  # Replace with your Raspberry Pi serial port

# def send_sms(phone_number, message):
#     with GsmModem(port= port, baudrate=115200) as modem:  # Adjust COM port and baud rate as needed
#         modem.connect()
#         modem.sendSms(phone_number, message)

def send_sms(phone_number, message):
    modem = GsmModem(port=port, baudrate=9600)  # Adjust COM port and baud rate as needed
    modem.connect()
    modem.sendSms(phone_number, message)
    modem.disconnect()  # Disconnect the modem when done



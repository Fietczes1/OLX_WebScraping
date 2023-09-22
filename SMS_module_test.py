import platform
import time
from gsmmodem.modem import GsmModem

from Sending_SMS_GSM_modem_liblary import send_sms

#Test the send_sms function
if __name__ == "__main__":
    phone_number = "+48721776456"  # Replace with the recipient's phone number
    message = "Hello, this is a test message from your GSM modem!"  # Your message

    try:
        send_sms(phone_number, message)
        print("Message sent successfully")
    except Exception as e:
        print(f"Error sending message: {e}")

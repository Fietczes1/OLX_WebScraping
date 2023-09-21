import serial
import time

def send_sms(phone_number, message_text):
    # Configure the serial port
    ser = serial.Serial('COM3', 9600, timeout=30)

    # Wait for the module to initialize
    time.sleep(5)

    try:
        # Set SMS text mode
        ser.write(b'AT+CMGF=1\r\n')
        time.sleep(3)  # Wait for 1 second
        response = ser.readline()
        print(response)

        # Enter recipient's phone number
        phone_number_cmd = f'AT+CMGS="{phone_number}"\r\n'.encode()
        ser.write(phone_number_cmd)
        time.sleep(30)  # Wait for 1 second
        response = ser.readline()
        print(response)

        # Enter message content and send
        message_cmd = f'{message_text}\x1A\r\n'.encode()
        ser.write(message_cmd)
        time.sleep(30)  # Wait for 1 second

        # Wait for response
        response = ser.readline()
        print(response)

    except Exception as e:
        print(f"Error sending message: {e}")

    finally:
        # Close the serial port
        ser.close()
        # Wait for response
        #response = ser.readline()
        #print(response)
        #time.sleep(30)

# Example usage:
if __name__ == "__main__":
    phone_number = "+48721776456"  # Replace with the recipient's phone number
    message = "Hello, this is a test message using the provided code!"  # Your message

    send_sms(phone_number, "1")
    time.sleep(30)
    send_sms('+48509520947',"1")
    time.sleep(30)
    send_sms(phone_number, "2")
    time.sleep(10)
    send_sms('+48509520947',"2")
    time.sleep(10)
    send_sms(phone_number, "3")
    time.sleep(5)
    send_sms('+48509520947',"3")
    time.sleep(5)
    send_sms(phone_number, "4")
    time.sleep(3)
    send_sms('+48509520947',"4")
    time.sleep(3)
    send_sms(phone_number, "5")
    send_sms('+48509520947',"5")

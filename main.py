import serial
from datetime import datetime

# Set up serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)

# Choose a file to save to
filename = "arduino_log_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"

# Open file in append mode
with open(filename, 'a') as file:
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            print("From Arduino:", line)
            file.write(line + '\n')  # Save line to file
        except Exception as e:
            print("Error:", e)
            break
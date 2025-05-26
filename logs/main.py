import serial

# Change 'COM4' to the correct port on your Windows system
ser = serial.Serial('COM4', 9600, timeout=1)

print("Listening on COM4... Press Ctrl+C to stop.")

with open("output.txt", "a") as file:
    try:
        while True:
            line = ser.readline()
            if line:
                decoded = line.decode('utf-8', errors='ignore').strip()
                print(f"Received: {decoded}")
                file.write(decoded + '\n')
                file.flush()
    except KeyboardInterrupt:
        print("\nStopped by user.")

ser.close()

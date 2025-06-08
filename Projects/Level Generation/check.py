import serial.tools.list_ports

def find_raspberry_pi_serial():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        desc = port.description.lower()
        if "raspberry" in desc or "usb serial" in desc:
            print(f"Possible Raspberry Pi detected on port: {port.device}")
            return
    print("Raspberry Pi not detected via USB serial.")

find_raspberry_pi_serial()

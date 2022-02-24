
import time, json
import board
import busio
 
import adafruit_gps


global topic
global mqtt_client

gps_data = dict()
gps_data['timestamp'] = ''
gps_data['satellites'] = 0
gps_data['latitude'] = 0.0
gps_data['longitude'] = 0.0
gps_data['altitude'] = 0.0


import serial
uart = serial.Serial("COM3", baudrate=9600, timeout=10)
 

gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

gps.send_command(b"PMTK220,1000")


last_print = time.monotonic()
data_topic = '/Mobius/UTM_UVARC/GPS'

while True:
    gps.update()
    current = time.monotonic()

    now = time.gmtime(time.time())

    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            print("Waiting for fix...")
            gps_data['timestamp'] = '{}/{}/{} {:02}:{:02}:{:02}'.format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            print(gps_data)
            gps_data = json.dumps(gps_data)
            # send_data_to_Mobius(data_topic, gps_data)
            gps_data = json.loads(gps_data)

            continue

        gps_data['timestamp'] = '{}/{}/{} {:02}:{:02}:{:02}'.format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        gps_data['satellites'] = int(gps.satellites)
        gps_data['latitude'] = float(gps.latitude)
        gps_data['longitude'] = float(gps.longitude)
        gps_data['altitude'] = float(gps.altitude_m)

        gps_data = json.dumps(gps_data)
        # send_data_to_Mobius(data_topic, gps_data)
        gps_data = json.loads(gps_data)
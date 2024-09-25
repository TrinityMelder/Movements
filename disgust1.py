from pythonosc import udp_client
import time

# Simulating idle state and then a sharp recoil for disgust
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 1000],  # Go to the idle position and pause briefly
]

positionx_neutral = 2500  # Neutral position (centered X-axis)
positionx_recoil = 2000  # Sharp recoil backward (X-axis)
positionx_jerk_forward = 2800  # Quick forward jerk (X-axis)

positiony_idle = 2500  # Neutral Y-axis (no vertical movement)

# Set up the OSC client
ip = "192.168.50.112"  # IP address of the OSC server
port = 9321            # Port of the OSC server
client = udp_client.SimpleUDPClient(ip, port)

def send_data(data):
    positionx, timex, positiony, timey = data[0]
    print('sending ', data[0])
    client.send_message("/bigbee", ['head', positionx, timex, positiony, timey])

    # Wait for the time specified
    wait_time = data[1]
    time.sleep(wait_time / 1000.0)  # Convert milliseconds to seconds

# Send the data to move to the idle state first
for data in to_send:
    send_data(data)

# Sharp recoil backward to simulate disgust
send_data([[positionx_recoil, 3100, positiony_idle, 300], 300])  # Fast recoil

# Quick jerk forward to emphasize rejection
send_data([[positionx_jerk_forward, 3200, positiony_idle, 200], 200])  # Quick jerk forward

# Return to neutral position
send_data([[positionx_neutral, 3000, positiony_idle, 300], 300])  # Back to neutral

print("Disgust movement (sharp recoil and jerk) completed.")

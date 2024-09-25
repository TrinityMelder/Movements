from pythonosc import udp_client
import time

# Simulating idle state and then a slow backward tilt followed by a faster forward jerk for surprise
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 1000],  # Go to the idle position and pause briefly
]

positionx_neutral = 2500  # Neutral position (centered)
positionx_tilt_back = 1800  # Move backward (tilting backward along X-axis)
positionx_pop_forward = 3200  # Sharp forward jerk for surprise

positiony_idle = 2500  # Fixed Y-axis for height during the movements

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

# Slow tilt backward to simulate surprise (moving along X-axis)
send_data([[positionx_tilt_back, 3100, positiony_idle, 500], 500])  # Tilt backward slowly

# Fast forward jerk for the surprise pop-up (moving quickly along X-axis)
send_data([[positionx_pop_forward, 3200, positiony_idle, 100], 100])  # Fast forward jerk

# Return to neutral position
send_data([[positionx_neutral, 3000, positiony_idle, 300], 300])  # Back to neutral

print("Surprise movement (backward tilt and fast jerk) completed.")

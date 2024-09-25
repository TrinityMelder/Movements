from pythonosc import udp_client
import time

# Simulating idle state and then abrupt side-to-side motion for disgust
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 1000],  # Go to the idle position and pause briefly
]

positionx_neutral = 2500  # Neutral X-axis
positionx_sway_left = 2200  # Sharp movement to the left
positionx_sway_right = 2800  # Sharp movement to the right

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

# Sharp movement to the left
send_data([[positionx_sway_left, 3000, positiony_idle, 200], 200])  # Fast movement to the left

# Sharp movement to the right
send_data([[positionx_sway_right, 3100, positiony_idle, 200], 200])  # Fast movement to the right

# Back to neutral
send_data([[positionx_neutral, 3000, positiony_idle, 300], 300])  # Return to neutral

print("Disgust movement (abrupt side-to-side) completed.")

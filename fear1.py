from pythonosc import udp_client
import time

# Simulating idle state and then a fast retreat followed by a pause for fear
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 1000],  # Go to the idle position and pause briefly
]

positionx_neutral = 2500  # Neutral X-axis
positionx_fast_back = 2000  # Fast retreat backward
positiony_idle = 2500  # Neutral Y-axis for height

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

# Fast retreat to simulate fear
send_data([[positionx_fast_back, 3200, positiony_idle, 200], 200])  # Fast retreat backward

# Pause, as if frozen in fear
time.sleep(2)  # Pause for 2 seconds, frozen in place

# Return to neutral position
send_data([[positionx_neutral, 3000, positiony_idle, 300], 300])  # Back to neutral

print("Fear movement (fast retreat and pause) completed.")

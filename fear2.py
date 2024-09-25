from pythonosc import udp_client
import time

# Simulating idle state and then jittery retreat for fear
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 1000],  # Go to the idle position and pause briefly
]

positionx_neutral = 2500  # Centered X-axis (neutral)
positionx_back = 2200  # Moving backward due to fear (X-axis)
positionx_forward = 2500  # Hesitant step forward
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

# Jittery backward and forward retreat to simulate fear
start_time = time.time()
duration = 10  # Movement lasts for 10 seconds

while time.time() - start_time < duration:
    send_data([[positionx_back, 3100, positiony_idle, 200], 200])  # Small retreat backward
    send_data([[positionx_forward, 3100, positiony_idle, 200], 200])  # Hesitant forward movement

print("Fear movement (jittery retreat) completed.")

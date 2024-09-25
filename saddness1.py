from pythonosc import udp_client
import time

# Simulating idle state and then a slow downward movement for sadness
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 1000],  # Go to the idle position and pause briefly
]

positionx_neutral = 2500  # Fixed X-axis (no lateral movement)
positiony_idle = 2500  # Start at neutral Y-axis
positiony_down = 1800  # Gradual downward movement for sadness

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

# Slow downward movement over 20 seconds to express sadness
start_time = time.time()
duration = 20  # Move slowly downward over 20 seconds

while time.time() - start_time < duration:
    # Gradually move downward in small steps
    positiony_step = positiony_idle - int((positiony_idle - positiony_down) * (time.time() - start_time) / duration)
    send_data([[positionx_neutral, 3000, positiony_step, 500], 500])  # Small downward step

print("Sadness movement (slow downward) completed.")

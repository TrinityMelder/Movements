from pythonosc import udp_client
import time

# Simulating idle state and then a small jump backward for surprise
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 500],  # Go to the idle position and pause briefly
]

positionx_neutral = 2500  # Neutral X-axis position
positionx_backward = 3200  # Backward movement on X-axis (opposite direction)
positiony_idle = 2500  # Y-axis remains neutral
positiony_jump = 1800  # Small upward jump for surprise

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

# Perform one small jump followed by a quick backward movement
jump_duration = 200  # Quick upward jump (200 milliseconds)
backward_duration = 500  # Backward movement duration (500 milliseconds)

# Move upward for a small jump
send_data([[positionx_neutral, jump_duration, positiony_jump, 1000], jump_duration])

# Move backward quickly
send_data([[positionx_backward, backward_duration, positiony_idle, 1000], backward_duration])

print("Small jump and backward movement for surprise completed.")

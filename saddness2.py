from pythonosc import udp_client
import time

# Simulating idle state and then drooping with side-to-side sway for sadness
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 1000],  # Go to the idle position and pause briefly
]

positionx_neutral = 2500  # Centered X-axis
positionx_sway_left = 2300  # Slight sway to the left
positionx_sway_right = 2700  # Slight sway to the right
positiony_down = 1800  # Drooping downward (Y-axis)

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

# Drooping with slight side-to-side sway over 20 seconds
start_time = time.time()
duration = 20  # Total duration for the movement

while time.time() - start_time < duration:
    # Sway to the left while drooping
    send_data([[positionx_sway_left, 3000, positiony_down, 1000], 1000])
    
    # Sway to the right while drooping
    send_data([[positionx_sway_right, 3000, positiony_down, 1000], 1000])

print("Sadness movement (drooping and swaying) completed.")

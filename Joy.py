from pythonosc import udp_client
import time

# Simulating idle state and then smooth up-and-down head waving on Y-axis for happiness
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 500],  # Go to the idle position and pause briefly
]

positionx_idle = 2500  # Fixed positionx (stable left/right)
positiony_min = 2000  # Less extreme downward movement
positiony_max = 3000  # Smooth upward movement

# Set up the OSC client
ip = "192.168.50.112"  # IP address of the OSC server
port = 9321            # Port of the OSC server
client = udp_client.SimpleUDPClient(ip, port)

def check_position_bounds(positiony):
    if not (positiony_min <= positiony <= positiony_max):
        print(f"Error: positiony {positiony} is out of bounds!")
        return False
    return True

def send_data(data):
    positionx, timex, positiony, timey = data[0]
    if not check_position_bounds(positiony):
        print("Skipping sending due to out-of-bound positions.")
        return
    print('sending ', data[0])
    client.send_message("/bigbee", ['head', positionx, timex, positiony, timey])

    # Wait for the time specified
    wait_time = data[1]
    time.sleep(wait_time / 1000.0)  # Convert milliseconds to seconds

# Send the data to move to the idle state first
for data in to_send:
    send_data(data)

# Time limit for the continuous movement (20 seconds)
start_time = time.time()
duration = 20  # Duration in seconds

# Continuously move up and down on Y-axis for 20 seconds to express happiness
while time.time() - start_time < duration:
    send_data([[positionx_idle, 3000, 3000, 600], 200])  # Smooth upward (Y-axis)
    send_data([[positionx_idle, 3000, 2000, 600], 200])  # Smooth downward (Y-axis)

print("20 seconds of happiness movement completed.")

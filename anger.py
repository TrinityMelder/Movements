from pythonosc import udp_client
import time

# Simulating idle state and then sharp side-to-side head movement to represent anger
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 500],  # Go to the idle position and pause briefly
]

positionx_min = 1800  # Minimum allowed positionx value (left-most)
positionx_max = 3200  # Maximum allowed positionx value (right-most)
positiony_idle = 2500  # Fixed positiony (stable up/down)

# Set up the OSC client
ip = "192.168.50.112"  # IP address of the OSC server
port = 9321            # Port of the OSC server
client = udp_client.SimpleUDPClient(ip, port)

def check_position_bounds(positionx):
    if not (positionx_min <= positionx <= positionx_max):
        print(f"Error: positionx {positionx} is out of bounds!")
        return False
    return True

def send_data(data):
    positionx, timex, positiony, timey = data[0]
    if not check_position_bounds(positionx):
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

# Time limit for the continuous movement (10 seconds for anger)
start_time = time.time()
duration = 10  # Duration in seconds (anger expressed quickly)

# Continuously move left and right sharply for anger with very short pauses
while time.time() - start_time < duration:
    send_data([[3200, 1000, positiony_idle, 100], 100])  # Sharp right with a quick motion
    send_data([[2500, 3000, positiony_idle, 100], 50])   # Short pause at idle
    send_data([[1800, 1000, positiony_idle, 100], 100])  # Sharp left with a quick motion
    send_data([[2500, 3000, positiony_idle, 100], 50])   # Short pause at idle

print("Anger movement completed.")

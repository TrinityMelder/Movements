from pythonosc import udp_client
import time

# Simulating idle state and then sharp sideways jerk followed by upward movement for surprise
to_send = [
    # Idle state (centered position)
    [[2500, 3000, 2500, 1000], 500],  # Go to the idle position and pause briefly
]

positionx_min = 1800  # Quick left-right jerk for surprise
positionx_max = 3200
positiony_idle = 2500  # Y-axis remains neutral for sideways jerk

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

# Time limit for surprise (5 seconds)
start_time = time.time()
duration = 5  # Quick short-lived surprise with left-right movement

# Sudden sharp left-right jerk followed by upward movement
while time.time() - start_time < duration:
    send_data([[3200, 3100, positiony_idle, 200], 100])  # Sharp right jerk
    send_data([[1800, 3200, positiony_idle, 200], 100])  # Sharp left jerk
    send_data([[2500, 3100, 3200, 300], 300])  # Sudden upward movement
    send_data([[2500, 3000, 2500, 200], 200])  # Return to neutral

print("Surprise movement (Set 2) completed.")

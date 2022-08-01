import argparse
import random
import time

from pythonosc import udp_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=39539,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient("127.0.0.1", 39540)

    for x in range(10):
        client.send_message("/VMC/Ext/Set/Eye", [1, random.uniform(-1,1), random.uniform(-1,1), random.uniform(-1,1)])
        time.sleep(1)

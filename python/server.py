from time import time
from typing import Optional

import numpy as np
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

from data_store import DataStore
from humanoid import Bone
from quaternion import Quaternion, vec3d, vec4d

def print_handler(address, *args):
    print(f"{address}: {args}")

def default_handler(address, *args):
    # print(f"DEFAULT {address}: {args}")
    if address == "/VMC/Ext/Bone/Pos":
        (label, x, y, z, qx, qy, qz, qw) = args
        bone = Bone( label, vec3d(x,y,z), Quaternion( vec4d(qx, qy, qz, qw) ) )
        DataStore.push(label, bone, label=="Head")
    else:
        pass
        # print(f"DEFAULT {address}: {args}")

class VmcServer:
    is_active: bool = False
    server: Optional[BlockingOSCUDPServer] = None

    def __init__(self):
        pass

    @classmethod
    def run(cls):
        print("VmcServer.run")
        dispatcher = Dispatcher()
        dispatcher.map("/something/*", print_handler )
        dispatcher.set_default_handler(default_handler )

        ip = "127.0.0.1"
        port = 1337
        # port = 39539

        cls.server = BlockingOSCUDPServer((ip, port), dispatcher)
        cls.is_active = True
        cls.server.serve_forever()  # Blocks forever

    @classmethod
    def stop(cls):
        if cls.server is not None:
            cls.server.shutdown()
            cls.server = None
            cls.is_active = False

if __name__ == "__main__":
    VmcServer.run()



from concurrent.futures import ThreadPoolExecutor
from threading import Event
import time

from data_store import DataStore
from server import VmcServer
from viewer import draw_anime, shutdown_viewer

def execute_tasks():
    exiting: Event = Event()
    executor = ThreadPoolExecutor(max_workers=3)

    view_task = executor.submit(draw_anime)
    store_task = executor.submit(DataStore.extract, exiting)
    server_task = executor.submit(VmcServer.run)

    
    try:
        while not exiting.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        exiting.set()

        view_task.cancel()
        store_task.cancel()
        server_task.cancel()

        shutdown_viewer()
        VmcServer.stop()
        executor.shutdown(wait=False)
        print('execute_tasks end')

if __name__ == "__main__":
    execute_tasks()
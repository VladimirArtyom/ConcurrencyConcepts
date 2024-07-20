# I m still learing this, so take it as a grain of salt
import os 
import time
import threading

from threading import Thread
# Thread itself is an inner Process 
# It is SHARED RESOURCES. It is dependent on the process resources, that managed by the OS
# Thread is managed by one process and able to communicate with other threads
# It is a light weight process. Becareful, if one thread fails, other threads will affected.Thread


def do_work(id: int) -> None :
    threadName: str = threading.current_thread().name
    print(f"{threadName} doing {id} work")
    time.sleep(4)
    print(f"{threadName} done {id} work")


def display_threads() -> None:
    print(f"Current Process: {os.getpid()}") # Process != Thread
    print(f"Total running threads: {threading.active_count()}")
    for thread in threading.enumerate():
        print(thread)

def main(n_threads: int) -> None:
    display_threads()

    print(f"Starting {n_threads} threads")
    for i in range(n_threads):
        thread: Thread = Thread(target=do_work, args=(i,))
        thread.start()

    display_threads()


if __name__ == "__main__":
    main(6)


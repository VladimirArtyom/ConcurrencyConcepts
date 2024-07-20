from queue import Queue # QUEUE Implements Locking Mechanism, therefore t
from threading import Thread, current_thread
import time

## Generally you're fine using any structure data for reading
# But when it comes to "Write"  YOu should ensure that the Write is only accessed by one thread. THAT WRITER Itself. 
# If any thread reading those. You need to move or suspend those reading threads.

class Worker(Thread):
    def __init__(this,queue: Queue, id: int):
        Thread.__init__(this)
        this.queue = queue
    
    def run(this) -> None:
        while not this.queue.empty():
            message = this.queue.get()
            time.sleep(3)
            print(f"Thread {current_thread().name}: \
                Received message: {message}")

class WorkerAnoher(Thread):
    def __init__(this,queue: list, id: int):
        Thread.__init__(this)
        this.queue = queue
        print(this.queue)
    
    def run(this) -> None:
        while not len(this.queue) == 0:
            message = this.queue.pop(0)
            time.sleep(3)
            print(f"Thread {current_thread().name}: \
                Received message: {message}")
def main(num_threads: int) -> None:
    queue = Queue()
    listBrah = []
    for i in range(5):
        listBrah.append(i)
        queue.put(i)

    threads = []
    for i in range(num_threads):
        #print("worker")
        #thread = Worker(queue, i+1)
        thread = WorkerAnoher(listBrah, i+1)

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main(10)

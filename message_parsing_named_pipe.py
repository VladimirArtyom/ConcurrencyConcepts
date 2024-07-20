from threading import Thread, current_thread
from multiprocessing import Pipe
from multiprocessing.connection import Connection


class Producer(Thread):
    def __init__(this, connection: Connection):
        super().__init__()
        this.name = "Producer"
        this.connection: Connection = connection
    
    def run(this) -> None:
        print(f"{current_thread().name} Sending message...")
        this.connection.send("Hello there")


class Consumer(Thread):
    def __init__(this, connection: Connection, id: int):
        super().__init__()
        this.name = f"Consumer {id}"
        this.connection: Connection = connection
    
    def run(this) -> None:
        print(f"{current_thread().name} Receiving message...")
        print(f"Received :{this.connection.recv()}")

def main() -> None:
    consumer_conn, producer_conn = Pipe()

    prod = Producer(producer_conn)
    consumer = Consumer(consumer_conn, 1)
    threads = [
        prod,
        consumer,
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

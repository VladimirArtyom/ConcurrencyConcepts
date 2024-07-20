from threading import Thread, current_thread
from multiprocessing import Pipe
from multiprocessing.connection import Connection


class Producer(Thread):
    def __init__(self, connection: Connection):
        super().__init__()
        self.name = "Producer"
        self.connection: Connection = connection

    def run(self) -> None:
        print(f"{current_thread().name} Sending message...")
        self.connection.send("Hello there")


class Consumer(Thread):
    def __init__(self, connection: Connection, id: int):
        super().__init__()
        self.name = f"Consumer {id}"
        self.connection: Connection = connection

    def run(self) -> None:
        print(f"{current_thread().name} Receiving message...")
        message = self.connection.recv()
        print(f"Received by {self.name}: {message}")


class Broadcaster(Thread):
    def __init__(self, input_conn: Connection, output_conns: list):
        super().__init__()
        self.input_conn = input_conn
        self.output_conns = output_conns

    def run(self) -> None:
        print(f"{current_thread().name} Broadcasting messages...")
        while True:
            message = self.input_conn.recv()
            for conn in self.output_conns:
                conn.send(message)


def main() -> None:
    producer_conn, broadcaster_conn = Pipe()

    consumer_conn1, output_conn1 = Pipe()
    consumer_conn2, output_conn2 = Pipe()
    consumer_conn3, output_conn3 = Pipe()
    consumer_conn4, output_conn4 = Pipe()

    prod = Producer(producer_conn)
    consumer1 = Consumer(consumer_conn1, 1)
    consumer2 = Consumer(consumer_conn2, 2)
    consumer3 = Consumer(consumer_conn3, 3)
    consumer4 = Consumer(consumer_conn4, 4)

    broadcaster = Broadcaster(broadcaster_conn, [output_conn1, output_conn2,
                                                 output_conn3, output_conn4])
    threads = [
        prod,
        consumer1,
        consumer2,
        consumer3,
        consumer4,
        broadcaster,
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()


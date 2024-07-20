import socket
import os
import errno
import time
from threading import Thread, current_thread
# You should not follow this approach when implementing message_parsing socket, 
# YOu thrive for concurrency . This code is blocking, especially the Consumer( SErver ) class
# Use timeouts if you want to, but its a hell to manage
SOCKET_FILE: str = "./mail.sock"
BUFFER_SIZE: str = 4096 # in Bytes
TIMEOUTS: int = 5 #  Wait for 5 seconds

class Producer(Thread):
    def __init__(this, id: int, messages):
        Thread.__init__(this)
        this.name = f"Producer {id}"
        this.messages = messages

    def run(this):

            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as socket_client:
                socket_client.connect((SOCKET_FILE)) # YOu can use the IP addr
                for message in this.messages:
                    socket_client.sendall(str.encode(message))
                    print(f"{current_thread().name}: Send: {message}")
class Consumer(Thread):
    def __init__(this, id: int):
        Thread.__init__(this)
        this.name = f"Consumer {id}"

    def run(this) -> None:

        socket_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) 
        socket_server.bind(SOCKET_FILE)
        socket_server.listen()

        socket_server.settimeout(TIMEOUTS)
        print(f"{current_thread().name}: Listening to incoming messages...")
        while True:
            conn, addr = socket_server.accept()
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                message = data.decode()
                print(f"{current_thread().name}: Received: {message}")
        socket_server.close()


def main() -> None:
    if os.path.exists(SOCKET_FILE):
        os.remove(SOCKET_FILE)

    messages: list = ["HI", "How Are You", "This from" ,f"Mr. Smith"]
    messages_2: list = ["Brah", "MAso", "Courrier" ,f"Mrs. Brenda"]
    messages_3: list = ["SOm", "YOUASH"]
    consumer = Consumer(1)
    
    producer = Producer(1, messages)
    producer_2 = Producer(2, messages_2)
    producer_3 = Producer(3, messages_3)
    
    threads = [
        producer_2,
        producer,
        producer_3

    ]
    consumer.start()

    producer.start()
    producer.join()
    time.sleep(4)
    producer_2.start()
    producer_2.join()
    time.sleep(10)
    producer_3.start()
    producer_3.join()


    consumer.join()

    os.remove(SOCKET_FILE)

if __name__ == "__main__":
    main()

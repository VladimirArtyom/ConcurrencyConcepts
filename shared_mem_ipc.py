import time
from threading import Thread, current_thread

# In shared memory, Thread can easily communicate. 
# Especially in case of producer-consumer problem, However consider using PIPE concept
# This apporach problematic
# 1. RACE Condition, You cannot be sure that the producer is writing same data to shared memory OR reading A LATEST data within the shared_memory. Consider pipe :D
# 2. It does not scale well. Because it is shared_memory, it is local bruh. Mostly used for local tasks. SMP system >< I don't know what that is right now

size: int = 10
shared_memory = [-1] * size
print(shared_memory)

class Producer(Thread):
    def __init__(self,  size: int):
        Thread.__init__(self)
        self.size = size
    def run(self):
        global shared_memory
        self.name = "Prod"
        for i in range(self.size):
            ##  Write data here, but how can you be sure that is not the same data written by the thread ? 
            # This is problematic when you building db for instance.
            print(f"{current_thread().name}: writing {int(i)}")
            shared_memory[i - 1] = i
        print(f"Producer: {shared_memory}")


class Consumer(Thread):
    def __init__(self, size: int):
        Thread.__init__(self)
        self.size = size
        
    def run(self):
        self.name = "Consumer"
        global shared_memory
        for i in range(self.size):
            while True:
                line = shared_memory[i]
                if line == -1:
                    print(f"{current_thread()}: Data is not available\n \
                    sleep 2 seconds, before trying")
                    time.sleep(2)
                    continue
                print(f"{current_thread()}: read {int(line)}")
                break


def main() -> None:
    threads = [
        Producer(size=size),
        Consumer(size=size)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()

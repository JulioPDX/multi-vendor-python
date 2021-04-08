#!/usr/bin/python3
# Credit to original author: Jimmy Taylor
# https://www.consentfactory.com/python-threading-queuing-netmiko/

import threading
from queue import Queue
from codetiming import Timer
from panos.base import PanDevice
from rich import print


# Set up thread count for number of threads to spin up
NUM_THREADS = 4
# This sets up the queue
enclosure_queue = Queue()
# Set up thread lock so that only one thread prints at a time
print_lock = threading.Lock()

USERNAME = "JulioPDX"
PASSWORD = "JulioPDX!"

timer = Timer()
timer.start()


def deviceconnector(num_thread, queue):
    """
    Function used in threads to connect to devices, passing in the thread # and queue
    """

    # This while loop runs indefinitely and grabs IP addresses from the queue and processes them
    # Loop will stop and restart if "ip_address = queue.get()" is empty
    while True:
        ip_address = queue.get()
        print(f"{num_thread}: Acquired IP: {ip_address}")
        try:
            print(f"Connecting to: {ip_address}")
            device = PanDevice.create_from_device(ip_address, USERNAME, PASSWORD)
            device_dict = dict()
            device_dict["hostname"] = device.show_system_info()["system"]["hostname"]
            device_dict["model"] = device.show_system_info()["system"]["model"]
            device_dict["version"] = device.get_device_version()
            print(device_dict)
            # device.restart()
            # print(f"Waiting for {ip_address}\n")
            # device.syncreboot()
            # print(f"[green]{ip_address} is online!!![/]")
        except:
            with print_lock:
                print(f"[red]Error connecting to {ip_address}[/]")
            queue.task_done()
        queue.task_done()


def main():
    """
    Main function that compiles the thread launcher and manages the queue
    """

    # Setting up threads based on number set above
    for num_thread in range(NUM_THREADS):
        # Create the thread using 'deviceconnector' as the function, passing in
        # the thread number and queue object as parameters
        thread = threading.Thread(
            target=deviceconnector,
            args=(
                num_thread,
                enclosure_queue,
            ),
        )
        # Set the thread as a background daemon/job
        thread.setDaemon(True)
        # Start the thread
        thread.start()
    hosts = ["192.168.10.143", "192.168.10.142"]
    # For each ip address in hosts
    for host in hosts:
        enclosure_queue.put(host)

    # Wait for all tasks in the queue to be marked as completed (task_done)
    enclosure_queue.join()
    print("*** Script complete")
    timer.stop()


if __name__ == "__main__":

    # Calling the main function
    main()

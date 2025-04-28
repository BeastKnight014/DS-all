from dateutil import parser
import threading
import socket
import time
import datetime
client_data = {}
def startReceivingClockTime(connector, address):
    while True:
        clock_time_string = connector.recv(1024).decode()
        clock_time = parser.parse(clock_time_string)
        client_data[address] = {
            "clock_time": clock_time  }
        print("Client Data updated with: " + str(address))
        time.sleep(5)
def startConnecting(master_server):
    while True:
        master_slave_connector, addr = master_server.accept()
        slave_address = str(addr[0]) + ":" + str(addr[1])
        print(slave_address + " got connected successfully")
        current_thread = threading.Thread(
            target=startReceivingClockTime,
            args=(master_slave_connector, slave_address)  )
        current_thread.start()
def synchronizeAllClocks():
    while True:
        print("New synchronization cycle started.")
        print("Number of clients: " + str(len(client_data)))
        if len(client_data) > 0:
            for client_addr, client in client_data.items():
                print(f"Client {client_addr} reported time: {client['clock_time']}")
        else:
            print("No client data. Synchronization not applicable.")
        print("\n\n")
        time.sleep(5)
def initiateClockServer(port=8080):
    master_server = socket.socket()
    master_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket at master node created successfully\n")
    master_server.bind(('', port))
    master_server.listen(10)
    print("Clock server started...\n")
    print("Starting to make connections...\n")
    master_thread = threading.Thread(
        target=startConnecting,
        args=(master_server,)  )
    master_thread.start()
    print("Starting synchronization parallelly...\n")
    sync_thread = threading.Thread(
        target=synchronizeAllClocks,
        args=()  )
    sync_thread.start()
if __name__ == '__main__':
    initiateClockServer(port=8080)
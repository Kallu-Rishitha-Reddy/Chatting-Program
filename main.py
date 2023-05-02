import threading
import socket
import os
import re

FORMAT = "utf-8"
SIZE = 1024

# Function to check whether the file name is in correct format or not
def check_filename(file):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    # Pass the string in search
    # Method of regex object
    if (regex.search(file) == None and file is not None):
        return False
    else:
        return True

# Function to write data from the file by breaking the file size into blocks of 1024 bytes
def receive_data(file, connect, total_size):
    data_sent = 0
    # Opening the file in write mode
    with open(file, 'wb+') as fileContent:
        while True:
            #dividing the data into blocks of 1024 byte size
            data_block = connect.recv(1024)
            #writing the data from the blocks into the file
            fileContent.write(data_block)
            data_sent = data_sent + len(data_block)
            #print("Server has received ",data_sent, "bytes")
            # Break the loop when the data sent is equal to total size of the file
            if total_size <= data_sent:
                break
    return data_sent

# Function to read data from the file by breaking the file size into blocks of 1024 bytes
def send_data(file, connect):
    data_sent = 0
    # Opening the file in read mode
    with open(file, 'rb+') as fileContent:
        while True:
            # Dividing the data into blocks of 1024 byte size
            data_block = fileContent.read(1024)
            if not data_block:
                break
            connect.sendall(data_block)
            data_sent = data_sent + len(data_block)
            #print("Server has sent ",data_sent, "bytes")
    return data_sent

# Function to read messages and file
def read_messages(socket):
    while True:
        try:
            # Receiving the socket message
            message = socket.recv(1024).decode()
            # Checking if the message starts with transfer
            if message.startswith("transfer"):
                #adding the file name into file after splitting
                file = message.split(" ")[1]
                f_name = os.path.join('files', f"new{file}")
                receiver = socket.recv(1024).decode(FORMAT)
                if 'SIZE' in receiver:
                    socket.send('OK'.encode(FORMAT))
                    total_size = int(receiver.split(' ')[1])
                    sent_bytes = receive_data(f_name, socket, total_size)
                    print("The transfer command is done. The receiver has received a total of", sent_bytes,
                          "bytes from the sender.")
            #Checking if the message is exit
            elif message == "exit":
                socket.close()
                break
            #in case of any other message
            else:
                print(message)
        except ConnectionAbortedError:
            socket.close()
            break

# Function to write messages and file
def write_messages():
    # Asking for the port number
    port = int(input("Enter the port: "))
    # Create a socket for writing
    writing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the port number given
    writing_socket.connect(("localhost", port))

    try:
        while True:
            message = input()
            # Checking if the message starts with transfer
            if message.startswith("transfer"):
                writing_socket.send(message.encode())
                file = message.split(" ")[1]
                f_name = os.path.join('files', file)
                # Checking if the file exists
                if os.path.exists(f_name):
                    # Getting the file size of the given file
                    file_size = os.path.getsize(f_name)
                    writing_socket.send(f"SIZE {file_size}".encode(FORMAT))
                    if writing_socket.recv(1024).decode(FORMAT) == 'OK':
                        sent_bytes = send_data(f_name, writing_socket)
                        print("The transfer command is done. The sender has sent a total of", sent_bytes,
                              "bytes to the receiver.")
                # Checking if the file name does not have any special characters in it
                elif check_filename(file):
                    print("Please enter valid file name")
                else:
                    print("The given file does not exist in the path")
            # Checking if the message is exit
            elif message == "exit":
                writing_socket.send(message.encode())
                writing_socket.close()
                break
            # in case of any other message
            else:
                writing_socket.send(message.encode())
    except:
        print("The connection will be shutting down now")
        # The socket will be closed
        writing_socket.send(message.encode())
        writing_socket.close()

def main():
    # Create a new thread for writing
    writing_thread = threading.Thread(target=write_messages, args=())
    writing_thread.start()

    # Create a socket for reading
    reading_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the reading socket
    reading_socket.bind(('localhost', 0))
    try:
        reading_socket.listen(1)
        # Print the port number for reading socket
        print("Listening on port ",reading_socket.getsockname())
        # Accept a connection for reading
        reading_connection, addr = reading_socket.accept()
        print(f"Connected to {addr}")
        # Read messages in the main thread
        read_messages(reading_connection)
        # Close the socket
        reading_connection.close()
    except KeyboardInterrupt:
        print("The connection between two users will be ended now")
        # End the connection of the client and server whenever a keyboard interrupt occurs
        reading_connection.close()
        return
    except:
        print("The connection will be shutting down now")
        # The socket will be closed
        reading_connection.close()

if __name__ == '__main__':
    main()

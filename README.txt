Implementation of Internet Chatting

Author: Rishitha Reddy Kallu
UFID: 20015890

Project Aim:
The task is to implement a chat program with multiple threads where the messages should show up on each other's windows and also in case of file transfer, it should be transferred

Language Used:
Python

Steps for Execution:
python main.py

Functionalities:
The three main functionalities implemented are as follows:
1. 'transfer <filename>': The file given will be transferred and stored locally as a new file
2. 'exit': The connection between both the user will be ended
3.  When a message is sent from one user, the message is displayed on the window of the other user

Workflow of the program:
1. First the main program is for the first user where a port number X is printed
2. The main program is run again for the second user where a port number Y is printed
3. Enter the port number Y for the first user
4. Enter the port number X for the second user
5. The message entered on first user's console window which should show on the second user's window
6. The message entered on second user's console window which should show on the first user's window
7. If the user enters transfer command with a file name from one user, then that file is taken from the path and transferred to the local storage with a new name
8. If the user enters exit, then the connection between the two users is closed
9. If a keyboard interrupt occurs, we handle the error by giving a prompt to the user and closing the connection
10. If any other exception occurs, the user will be prompted with a message and the connection is closed

Output:
User 1 Console Window:
Enter the port: Listening on port  ('127.0.0.1', 62983)
62986
Connected to ('127.0.0.1', 62988)
hi I am A
hello I am B
The transfer command is done. The receiver has received a total of 1780871 bytes from the sender.
exit

Process finished with exit code 0

User 2 Console Window:
Enter the port: Listening on port  ('127.0.0.1', 62986)
Connected to ('127.0.0.1', 62987)
62983
hi I am A
hello I am B
transfer testFile1.pptx
The transfer command is done. The sender has sent a total of 1780871 bytes to the receiver.
exit

Process finished with exit code 0

Result:
Finally, using multi threads, two users simultaneously are run and messages are sent to each other and transferring a file are done successfully.

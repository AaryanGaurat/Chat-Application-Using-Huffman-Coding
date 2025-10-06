
Chat Application Using Huffman Coding

A real-time, multi-client chat application built with Python that demonstrates the practical application of Huffman coding for data compression over a network. The project features a server, a user-friendly graphical client built with Tkinter, and an integrated, real-time visualizer to break down the compression process.
Chat Application Using Huffman Coding

An example of the GUI chat client in action with multiple users.
<img width="1918" height="1025" alt="image" src="https://github.com/user-attachments/assets/a7d3f0f3-7ca4-491e-b554-a6eb49f625f0" />
<img width="559" height="730" alt="image" src="https://github.com/user-attachments/assets/0e560073-c725-44a3-bd4f-3f2c528147dc" />


Core Concepts

This project integrates several key computer science concepts:

    Huffman Coding: A lossless data compression algorithm that uses variable-length codes for characters based on their frequency of appearance. This is the core of the project's bandwidth-saving feature.

    Client-Server Architecture: A classic networking model where a central server manages connections and data flow between multiple clients.

    Socket Programming: Utilizes Python's socket library to establish and manage low-level network connections (TCP/IP) between the server and clients.

    Multithreading: The server uses Python's threading library to handle multiple client connections simultaneously, ensuring the application is non-blocking and responsive.

    GUI Development: The client interface is built using Tkinter, Python's standard library for creating graphical user interfaces.

Features

    Real-time, Multi-Client Chat: Supports an unlimited number of clients chatting in a single room.

    Dynamic Data Compression: All text messages are compressed using Huffman coding before being sent over the network, reducing bandwidth usage.

    Live Compression Visualizer: A unique, integrated tool that opens in a separate window to provide a detailed, step-by-step breakdown of the Huffman compression process for any message sent or received.

    User-Friendly Graphical Interface: A clean and modern GUI built with Tkinter, providing a much better user experience than a standard terminal application.

    Robust Server: The server is designed to gracefully handle clients connecting and disconnecting abruptly.
     

Prerequisites

Before you begin, ensure you have the following installed on your system:

    Python 3: Version 3.7 or newer is recommended.

That's it! The project is built using only Python's standard libraries, so no additional packages (pip install) are required.
Installation & Setup

Clone the repository (or download the ZIP):

    git clone [https://github.com/YourUsername/huffman-chat-application.git](https://github.com/YourUsername/huffman-chat-application.git)

    
(Replace YourUsername/huffman-chat-application.git with your actual repository URL)

 Navigate to the project directory:
   
    cd Chat-Application-Using-Huffman-Coding

Usage

1. Start the Server

Open a terminal or command prompt in the project directory and run the following command:
```
python chat_server.py
```

The server will start and print a message indicating it is waiting for client connections. Keep this terminal window open.
2. Start a Chat Client

For each user you want to add to the chat, open a new, separate terminal and run the following command:
```
python chat_client.py
```
A graphical window will appear, prompting you to enter a username. After entering a name, the main chat window will open and connect you to the server. You can repeat this step to open multiple client windows.
	
Developed By

    Sarthak Bari

    Sujal Chavan

    Aaryan Gaurat

    Varad Chaudhari

This project is distributed under the MIT License. See the LICENSE file for more information.

## Software Design Document

The purpose of this document is provide a detailed description of the implementation of the File Transfer Service as per required by the project description. This application partially emulates the service provided for file transfer protocols and follows its defined standards for encoding and transporting data between the client adn server.

### Scope
This project consists of two applications, tcp_client and tcp_server. Since both programs share common functionalities, the implementation has been divided into different packages under the `ftp` namespace which they both make use of. The list of implemented modules are provided below: 

- cmd
  - arguments
- parser
  - message_type
  - message
  - packet
- tcp
  - client
  - server

Furthermore, some of the above modules depends on external packages which should be properly installed with the help of a package manager.
- autopep8==1.6.0
- bitarray-ph4==1.9.1
- importlib-metadata==4.11.3
- Mako==1.2.0

A complete list of required packages is provided in the `requirements.txt` text file.

### Design Overview
The file transfer protocol provides a set of standard communication protocol used for sending and receiving files over the network. The connection should be established between a client and server, and the communication should be done over a secure channel where data is transfered. The data sent is usually encapsulated by a packet which contains the information that the device wish to transmit. Such data is expected to follow a sequence of request and response message flow, so both devices can properly communicate with each other. The following list defines the set of request-response message expected by both server and client.  
|Request|Header|
|---|---|
|put name|000|
|get name|001|
|change old new|010|
|help|011|

|Response|Header|
|---|---|
|ok put or change|000|
|ok get|001|
|error not found|010|
|error unknown|011|
|help|110|

### Technology Used
The implementation of both application has been done using the Python3's socket API which provides several functions and methods to perform IPC communications over the network.  

### System Architecture
The file transfer servioce is constructed over a set of defined objects, each defining a specific type or set of behavior. Both clients and servers use a well-defined packet type to communicate with each other. Therefore, in order to properly evaluate this communication, each packet sent or received are properly parsed and converted to a known bit representation, which is then verified against the set of expected Response or Request message. 

- Message Type:
Provides the defintion of each Method used in this system
- Message:
Object that represents the data used during FTP communication. Also provides an utility class that provides helper functions.
- Packet:
Object that is represented as a string of bit values
- Client:
TCP Client algorithm and logic
- Server:
TCP Server algorithm and logic
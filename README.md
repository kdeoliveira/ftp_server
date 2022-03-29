<p align="center"> 
  <img src="https://www.qnx.com/style-v2/img/bb-qnx-logo.png" alt="qnx"/>
  <img src="https://www.qt.io/hubfs/qt-design-system/assets/logos/qt-logo.svg" width="100" alt="qt">
</p>


## Real Time Application of Vehicule Monitoring System
This project involves all or part of the design, implementation, testing, and analysis of a simplified
real-time system for monitoring of vehicle’s health conditions.

### Overview

- The application consist of two parts, an FTP Client and FTP Server
- The main purpose of these client/server programs is to give the client the ability to download files from the server directory to the client directory and upload files from the client directory to the server directory
- All required packages for this project are provided in the requirement text file
- Note that in order to built the GUI using GCC, the proper qmake tool needs to be generated from the Qt source files.

### Requirements
- Python 3
- Required packages installed


### Running on QNX VM 
Before execution, make sure the main directory for both server and client are created  

To run the server: ``tcp_server.py``  
To run the client: ``tcp_client.py``  

The list of available commands can be found by passing any of those help arguments ``-h`` ``--help`` ``-?``  

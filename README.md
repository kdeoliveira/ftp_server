<p align="center"> 
  <img src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png" width="100" alt="py"/>
  <img src="https://blitapp.com/blog/articles/save-web-captures-to-ftp-server/ftp.png" width="100" alt="ftp">
</p>


## Network Application Development for File Transfer Service 
Develop a pair of client-server programs that communicate via Python stream sockets and simulate partially the file transfer protocol (FTP). The main purpose of these client/server programs is to give the client the ability to download files from the server directory to the client directory and upload files from the client directory to the server directory. We should be able to transfer any file type such as txt, doc, jpg.

### Overview

- The application consist of two parts, an FTP Client and FTP Server
- The main purpose of these client/server programs is to give the client the ability to download files from the server directory to the client directory and upload files from the client directory to the server directory
- All required packages for this project are provided in the requirement text file

### Requirements
- Python 3
- Required packages installed (requirements.txt)


### Running
Before execution, make sure the main directory for both server and client are created  

To run the server: ``tcp_server.py``  
To run the client: ``tcp_client.py``  

The list of available commands can be found by passing any of those help arguments ``-h`` ``--help`` ``-?``  

Below you can find the set of arguments available for both applications.

- -d: Activate Debug mode
- -a `addr`: Address which socket should connect to. Default value is localhost (127.0.0.1)
- -p `arg`: Port number which socket should attach its connection. Default value is 1025
- -F `arg`: Relative path used by the application
- -f `arg`: Absolute path used by the application

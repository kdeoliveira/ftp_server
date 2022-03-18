
from ftp.cmd import arguments
from ftp.parser.message_type import MessageType, RequestType, ResponseType
from ftp.parser.message import Message
from ftp.tcp.server import TcpServer

cmd = arguments.ParserArgs(2, helper = "Error", version="new version 1.0")

cmd.get_args()

arr = cmd.parameters(["-v"])


tcp_server = TcpServer("127.0.0.1")

tcp_server.listen()


parser = Message(3,  RequestType.CHANGE)


# parser.token(
#     [4, 3]
# )

parser.parse("0101100111")


print(      parser, ResponseType( "000" )     )
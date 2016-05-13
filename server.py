from packages.avs import Server

server = Server(1)
server.connect('172.28.128.3', 5000)
server.start('127.0.0.1', 5000)

import xmlrpc.client

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://localhost:9000')

string = "hello world"

print(server.string_reverse(string))
print(server.string_length(string))
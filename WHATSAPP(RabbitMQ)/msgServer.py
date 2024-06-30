import zmq

class MessageServer:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:3000")

        # Initialize an empty dictionary to store group servers
        self.group_servers = {}
        print(self.group_servers)
    def handle_requests(self):
        print("Message server is now listening on port 3000...")
        while True:
            message = self.socket.recv_string()
            parts = message.split()
            command = parts[0]
            if command == "registerGroupServer":
                server_name = parts[1]
                ip_address = parts[2]
                # Register group server
                if server_name in self.group_servers:
                        print(f"Group Already Exist  {server_name} [{ip_address}]")
                        self.socket.send_string("FAIL")
                    
                else:
                    self.group_servers[server_name]=ip_address
                    print(self.group_servers)
                    # Print success message---
                    print(f"JOIN REQUEST FROM {server_name} [{ip_address}]")
                    self.socket.send_string("SUCCESS")

            elif command == "getGroupList":
                # Send list of group servers to user
                group_list = "\n".join([f"{server_name} - {ip_address}" for server_name, ip_address in self.group_servers.items()])
                print("GROUP LIST REQUEST FROM CLIENT")
                self.socket.send_string(group_list)

            else:
                self.socket.send_string("INVALID COMMAND")

def main():
    message_server = MessageServer()
    message_server.handle_requests()

if __name__ == "__main__":
    main()

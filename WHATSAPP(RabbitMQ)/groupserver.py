import zmq
import time
from datetime import datetime
import threading
class GroupServer:
    def __init__(self, server_name, port):
        self.server_name = server_name
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{port}")

        # Initialize an empty dictionary to store group memberships
        self.group_memberships = {}

        # Initialize an empty dictionary to store group messages
        self.group_messages = {}
    
    def register_with_message_server(self):
        message = f"registerGroupServer {self.server_name} {self.port}"
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://34.125.84.69:3000")
        socket.send_string(message)
        response = socket.recv_string()
        return response
    def getMessage(self,group_id,user_id,parts):
        if group_id in self.group_messages:
            if user_id in self.group_memberships[group_id]:
                if len(parts)>3:
                    timestamp = parts[3] + " " + parts[4]
                    format="%Y-%m-%d %H:%M:%S"
                    print(timestamp)
                    print( self.group_messages[group_id])
                    messages = [msg for msg in self.group_messages[group_id] if datetime.strptime(msg["timestamp"], format) >=datetime.strptime(timestamp,format)]
                else:
                    print("typing msg")
                    messages = self.group_messages[group_id]
                # Success message
                print(f"MESSAGE REQUEST FROM {user_id} [{self.server_name}]")
                self.socket.send_string("\n".join([msg["message"] for msg in messages]))
            else:
                self.socket.send_string("You are not the member of this group")
                print("User not member of the group")    
        else:
            self.socket.send_string("No messages found in the group") 
    def sendMessage(self,group_id,user_id,parts):
        if group_id not in self.group_messages and user_id in self.group_memberships[group_id]:
                        self.group_messages.setdefault(group_id,[])
                        self.group_messages[group_id].append({"user_id": user_id, "message": " ".join(parts[3:]), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    # Success message
                        print(f"MESSAGE SEND FROM {user_id} [{self.server_name}]")
                        self.socket.send_string("SUCCESS")
        elif group_id in self.group_memberships and user_id in self.group_memberships[group_id]:
            # Add message to group's message list with timestamp
            
            self.group_messages[group_id].append({"user_id": user_id, "message": " ".join(parts[3:]), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            # Success message
            print(f"MESSAGE SEND FROM {user_id} [{self.server_name}]")
            self.socket.send_string("SUCCESS")
        else:
            self.socket.send_string("FAIL")  # If user not found in the group

           
    def handle_requests(self):
        while True:
            message = self.socket.recv_string()
            parts = message.split()
            command = parts[0]
            user_id = parts[1]
            group_id = parts[2]

            if command == "joinGroup":
                # Add user to the group's USERTELE
                if group_id not in self.group_memberships:
                    self.group_memberships.setdefault(group_id,[])
                    self.group_memberships[group_id].append(user_id)
                    print(f"JOIN REQUEST FROM {user_id} [{self.server_name}]")
                    self.socket.send_string("SUCCESS")
                
                elif group_id in self.group_memberships:
                    if user_id not in self.group_memberships[group_id]:
                        self.group_memberships.setdefault(group_id,[])
                        self.group_memberships[group_id].append(user_id)
                        print(f"JOIN REQUEST FROM {user_id} [{self.server_name}]")
                        self.socket.send_string("SUCCESS")
                    else:
                        print(f"Already a Group User {user_id} [{self.server_name}]")
                        self.socket.send_string("Fail")
                else :
                    self.socket.send_string("Fail")

            
            elif command == "leaveGroup":
                # Remove user from the group's USERTELE
                if group_id in self.group_memberships and user_id in self.group_memberships[group_id]:
                    self.group_memberships[group_id].remove(user_id)
                    # Success message
                    print(f"LEAVE REQUEST FROM {user_id} [{self.server_name}]")
                    self.socket.send_string("SUCCESS")
                else:
                    self.socket.send_string("FAIL")  # If user not found in the group

            elif command == "getMessages":
                t =threading.Thread(target=self.getMessage,args=(group_id,user_id,parts))
                t.start()
                t.join()
                 # If no messages found

            elif command == "sendMessage":
                t1 =threading.Thread(target=self.sendMessage,args=(group_id,user_id,parts))
                t1.start()
                t1.join()
                # Check if user is part of the group
            else:
                self.socket.send_string("INVALID COMMAND")

def main():
    servername=input("Enter the name for your server:")
    Group_port=input("Enter the Group port:")
    group_server = GroupServer(servername,Group_port)
    response = group_server.register_with_message_server()
    print("GroupServer Registration Response:", response)
    group_server.handle_requests()

if __name__ == "__main__":
    main()
#https://chat.openai.com/share/9cda49f2-fe6d-4fdd-a8c6-da280c6a1ea1
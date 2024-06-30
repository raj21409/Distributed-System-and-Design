import zmq
import uuid
unique_id = str(uuid.uuid1())
              
class UserClient:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
          # Connect to the message server

    def get_group_list(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        
        socket.connect("tcp://34.125.84.69:3000")
        socket.send_string("getGroupList")
        group_list = socket.recv_string()
        return group_list

    def join_group(self, user_id, group_id):
        message = f"joinGroup {user_id} {group_id}"
        self.socket.connect(f"tcp://34.16.176.150:{group_id}")
        self.socket.send_string(message)
        response = self.socket.recv_string()
        return response

    def leave_group(self, user_id, group_id):
        message = f"leaveGroup {user_id} {group_id}"
        self.socket.send_string(message)
        response = self.socket.recv_string()
        return response

    def send_message(self, user_id, group_id, message):
        message = f"sendMessage {user_id} {group_id} {message}"
        self.socket.connect(f"tcp://34.16.176.150:{group_id}")
        self.socket.send_string(message)
        response = self.socket.recv_string()
        return response

    def get_messages(self, user_id, group_id, timestamp=None):
        if timestamp:
            message = f"getMessages {user_id} {group_id} {timestamp}"
        else:
             message = f"getMessages {user_id} {group_id}"
        self.socket.send_string(message)
        messages = self.socket.recv_string()
        return messages
    
       
def main():
    user_client = UserClient()
    user_id = str(uuid.uuid1()) 
     # Example group Port ID
    while(True):
        print("Menu:")
        print("1. Get Group List")
        print("2. Join Group")
        print("3. Leave Group")
        print("4. Send Message")
        print("5. Get Messages")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice=="1":
            group_list = user_client.get_group_list()
            print("Available Groups:")
            print(group_list)
            
        elif choice=="2":
            group_id = input("Enter the Group Port Number:")
            join_response = user_client.join_group(user_id, group_id)
            print("Join Group Response:", join_response)
        elif choice=="3":
            group_id = input("Enter the Group Port Number:")
            join_response = user_client.leave_group(user_id, group_id)
            print("Leave Group Response:", join_response)
        elif choice=="4":
            group_id = input("Enter the Group Port Number:")
            message1=input("Enter the message here:")
            msg_response = user_client.send_message(user_id, group_id,message1)
            print("Message Group Response:", msg_response)
        elif choice=="5":
            group_id = input("Enter the Group Port Number:")
            timestamp1=input("Enter the TimeStamp:")
            if timestamp1!="":
                msg_response = user_client.get_messages(user_id, group_id,timestamp1)
                print("Get Message Group Response:", msg_response)
            else:
                msg_response = user_client.get_messages(user_id, group_id)
                print("Get Message Group Response:", msg_response)
        elif choice == "6":
            print("Exiting...")
            break
        

    # message_response = user_client.send_message(user_id, group_id, "Hello, Group!")
    # print("Send Message Response:", message_response)

    # leave_response = user_client.leave_group(user_id, group_id)
    # print("Leave Group Response:", leave_response)

if __name__ == "__main__":
    main()

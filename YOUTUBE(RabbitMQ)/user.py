import json
import sys
import pika

def initialize_user():
    user_name = sys.argv[1]

    if( len(sys.argv) > 3):
        youtuber = sys.argv[3]
    else:
        youtuber=None

    if(len(sys.argv) > 2) :
        action = sys.argv[2]
    else :
        action=None

    user = UserAgent(user_name, action, youtuber)
    return user

class UserAgent:
    def __init__(self, user_name, action=None, youtuber=None):
        info=pika.PlainCredentials('guest','guest')
        parameters=pika.ConnectionParameters('34.66.142.215',5672,'/',info)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.user_name = user_name
        self.channel.queue_declare(queue=self.user_name)
        self.youtuber = youtuber
        self.action = action
        self.personal_queue = self.user_name

    def update_subscription(self):
        if self.action == ("u" or "U"):
            subscribe = False
            print(f"{self.user_name} unsubscribed from {self.youtuber}")
        elif self.action == ("s" or "S") :
            subscribe = True
            print(f"{self.user_name} subscribed to {self.youtuber}")

        self.channel.queue_declare(queue='media_main')
        rt_key = 'media_main'
        self.channel.basic_publish(
            exchange='',
            routing_key=rt_key,
            body=json.dumps({"user": self.user_name, "action": "subscription", "youtuber": self.youtuber, "subscribe": subscribe})
        )
        print("Subscription updated")

    def receive_notifications(self, ch, method, properties, body):
        notification = json.loads(body.decode())
        print(f"New notification recieved {notification['youtuber']} has uploaded {notification['video_name']}")

    def perform_action(self):
        if self.action == "s":
            self.update_subscription()
        elif self.action == "u":
            self.update_subscription()
        else:
            print(f"{self.user_name} is now logged in")

    def run(self):
        self.perform_action()
        if self.action is None:
            self.channel.basic_consume(queue=self.personal_queue, on_message_callback=self.receive_notifications, auto_ack=True)
            print(f"{self.user_name} is waiting for notifications")
            self.channel.start_consuming()

user = initialize_user()
user.run()
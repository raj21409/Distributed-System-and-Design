import json
import sys
import pika

class MediaServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.user_queues = {}
        self.subscribers = {}
        self.subs={}
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='media_youtubers')
        self.channel.queue_declare(queue='media_main')
        self.channel.basic_consume(queue='media_youtubers', on_message_callback=self.consume_media_requests, auto_ack=True)
        self.channel.basic_consume(queue='media_main', on_message_callback=self.handle_client_requests, auto_ack=True)
        print("youtube server is now listening for requests")
        self.channel.start_consuming()



    def handle_client_requests(self,ch, method, properties, body):
        request = json.loads(body.decode())
        action = request.get("action", None)

        if(action == "subscription"):
            # self.handle_subscription(request)
            user = request["user"]
            youtuber = request["youtuber"]
            sucubscribe=(user,youtuber)
            self.subs[user]=youtuber
            subscribe = request["subscribe"]
            print(sucubscribe)
            if youtuber not in self.subscribers:
                self.subscribers[youtuber] = []
            if youtuber in self.subs:
                self.subscribers[youtuber] = []
            if subscribe:
                self.subscribers[youtuber].append(user)
                print(f"{user} has subscribed to {youtuber}")
            else:
                self.subscribers[youtuber].remove(user)
                print(f"{user} has unsubscribed from {youtuber}")
        elif action == "upload":
            # self.handle_video_upload(request)
            youtuber = request["youtuber"]
            video_name = request["video_name"]
            # self.notify_subscribers(youtuber, video_name)
            if youtuber in self.subscribers:
                for user in self.subscribers[youtuber]:
                    user1=user
                    self.channel.basic_publish(
                        exchange='',
                        routing_key=user,
                        body=json.dumps({"youtuber": youtuber, "video_name": video_name})
                    )
                    print(user1)
            print(f"{youtuber} has uploaded {video_name}")
        else:
            print("Invalid action:", action)



   

    def consume_media_requests(self, ch, method, properties, body):
        request = json.loads(body.decode())
        youtuber = request["youtuber"]
        
        video_name = request["video_name"]
        self.subs[video_name]=youtuber
        if youtuber not in self.subscribers:
            self.subscribers[youtuber] = []

        for user in self.subscribers[youtuber]:
            self.channel.basic_publish(
                exchange='',
                routing_key=user,
                body=json.dumps({"youtuber": youtuber, "video_name": video_name})
            )


media_server = MediaServer()
# media_server.run_queries()
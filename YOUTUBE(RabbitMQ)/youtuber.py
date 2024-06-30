import json
import sys
import pika

class ContentCreator:
    def __init__(self, creator_name, content_name):
        info=pika.PlainCredentials('guest','guest')
        parameters=pika.ConnectionParameters('34.66.142.215',5672,'/',info)
        self.connection = pika.BlockingConnection(parameters)
        self.content_name = content_name
        self.creator_name = creator_name
        self.channel = self.connection.channel()

    def upload_content(self):
        rt_key = 'media_main'
        self.channel.basic_publish(
            exchange='',
            routing_key=rt_key,
            body=json.dumps({"creator": self.creator_name, "content_name": self.content_name, "action": "upload"})
        )
        print("Video successfully uploaded")

creator = ContentCreator(sys.argv[1], sys.argv[2])
creator.upload_content()
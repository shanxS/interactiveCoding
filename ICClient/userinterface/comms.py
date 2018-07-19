import boto3
from userinterface.printer import Printer
import time

"""
This layer is used for end user to ICClient communication.
"""


class VoiceRequestPuller:
    def __init__(self, queueName, profileName, logger):
        session = boto3.Session(profile_name=profileName)
        # Get the service resource
        sqs = session.resource('sqs')
        # Get the queue
        self.queue = sqs.get_queue_by_name(QueueName=queueName)
        self.log = logger

    def getMessage(self):
        for message in self.queue.receive_messages(WaitTimeSeconds=5):
            if (message):
                message.delete()
                self.log.debug(log="Received from lambda ", cmd=message.body, result="")

                return message.body


class VoiceResponsePusher:
    def __init__(self, queueName, profileName, logger):
        session = boto3.Session(profile_name=profileName)
        # Get the service resource
        sqs = session.resource('sqs')
        # Get the queue
        self.queue = sqs.get_queue_by_name(QueueName=queueName)
        self.log = logger

    def sendMessage(self, message):
        uun = str(time.time())
        self.queue.send_message(MessageBody=message, MessageGroupId='1', MessageDeduplicationId=uun)

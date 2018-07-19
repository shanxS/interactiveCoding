import boto3


class Reader:
    def __init__(self, queueName, profileName):
        session = boto3.Session(profile_name=profileName)
        # Get the service resource
        sqs = session.resource('sqs')
        # Get the queue
        self.queue = sqs.get_queue_by_name(QueueName=queueName)

    def getMessage(self):
        # Process messages by printing out body
        for message in self.queue.receive_messages(WaitTimeSeconds=5):
            if (message):
                print(message.body)
                message.delete()

                return message.body

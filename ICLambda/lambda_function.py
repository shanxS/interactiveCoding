import boto3
import json
import time


def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'])

    return build_response()


def on_launch(request):
    return build_response(dialog="Start by setting a project.", shouldEndSession=False)


def on_intent(request):
    send_to_user(request)
    if 'name' in request['intent'] and request['intent']['name'] == 'AMAZON.StopIntent':
        return build_response(dialog="", shouldEndSession=True)
    else:
        return build_response(dialog="", shouldEndSession=False)


def on_session_ended(request):
    send_to_user(request)
    return build_response(dialog="", shouldEndSession=True)


def send_to_user(request):
    sqs = boto3.resource('sqs')

    queue = sqs.get_queue_by_name(QueueName='coder_queue_request.fifo')

    uun = str(time.time())
    queue.send_message(MessageBody=json.dumps(request), MessageGroupId='1', MessageDeduplicationId=uun)


def build_response(dialog, shouldEndSession):
    response = {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            "outputSpeech": {
                "type": "PlainText",
                "text": dialog
            },
            "shouldEndSession": shouldEndSession
        }
    }

    if (dialog == ''):
        del response['response']['outputSpeech']

    return response

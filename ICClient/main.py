from userinterface.printer import Printer
from userinterface.comms import VoiceRequestPuller, VoiceResponsePusher
from userinterface.userfeedbackprovider import UserFeedbackProvider
from localexecutor import LocalExecutor
import argparse
from parser.lambdaparser import LambdaParser
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="print debug logs", action="store_true")
    args = parser.parse_args()

    ioc(args)

    while True:
        lambdaData = voiceConsumer.getMessage()
        if (lambdaData):
            executor.execute(lambdaparser.parse(json.loads(lambdaData)))


def ioc(args):

    debug = False
    if args.debug:
        debug = True

    printer = Printer(isDebugMode=debug)

    global voiceConsumer
    voiceConsumer = VoiceRequestPuller(queueName='coder_queue_request.fifo', profileName='endReader', logger=printer)

    voiceProducer = VoiceResponsePusher(queueName='coder_queue_response.fifo', profileName='endReader', logger=printer)

    userFedbackProvider = UserFeedbackProvider(voiceFeedbackProvider=voiceProducer, textFeedbackProvider=printer)

    global executor
    executor = LocalExecutor(userFedbackProvider=userFedbackProvider, logger=printer)

    global lambdaparser
    lambdaparser = LambdaParser(userFedbackProvider=userFedbackProvider, logger=printer)


if __name__ == "__main__":
    # execute only if run as a script
    main()

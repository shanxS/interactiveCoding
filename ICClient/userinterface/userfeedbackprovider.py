"""
This layer is used to send feedback to end user, via text and voice interface
"""


class UserFeedbackProvider:
    def __init__(self, voiceFeedbackProvider, textFeedbackProvider):
        self.voiceFeedbackProvider = voiceFeedbackProvider
        self.textFeedbackProvider = textFeedbackProvider

    def send(self, msg, requestId):
        self.textFeedbackProvider.print("", msg, "")

        voiceFeedback = {}
        voiceFeedback['requestId'] = requestId
        voiceFeedback['msg'] = msg

        self.voiceFeedbackProvider.sendMessage(str(voiceFeedback))

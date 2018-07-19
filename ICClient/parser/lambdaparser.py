from utils.const import *
from utils.cmdtypes import *
import locale

"""
This layer is reponsible for converting user's uttreance to final 
executable cmd. Cmds are of types described in cmdtypes module.

Few generations down the line this part will be done using ML.
"""


class LambdaParser:
    def __init__(self, userFedbackProvider, logger):
        self.userFedbackProvider = userFedbackProvider
        self.log = logger

    def parse(self, lambdaData):
        if lambdaData['type'] == 'LaunchRequest':
            self.log.error("Parser", "Not expecting LaunchRequest intent", "")

        elif lambdaData['type'] == 'IntentRequest':
            if 'slots' in lambdaData['intent']:
                return self._parseIntentRequest(slots=lambdaData['intent']['slots'], requestId=lambdaData['requestId'])
            elif 'name' in lambdaData['intent'] and lambdaData['intent']['name'] == CONST.stopIntent:
                return CONST.end_session

        elif lambdaData['type'] == 'SessionEndedRequest':
            return CONST.end_session

        else:
            self.log.print("Parser", "Not expected intent type ", lambdaData)
            return CONST.invalid

    def _parseIntentRequest(self, slots, requestId):

        if CONST.projectNameSlot in slots:
            self.isProjectSet = True
            return SetProjectNameCmd(slots[CONST.projectNameSlot]['value'], requestId)

        elif CONST.emptySlot in slots:
            userInput = slots[CONST.emptySlot]['value']
            return RawCmd(userInput, requestId)

        elif (CONST.relativeDirNameSlot in slots) or (CONST.dirNameSlot in slots):
            if ('value' in slots[CONST.relativeDirNameSlot]) and ('value' in slots[CONST.dirNameSlot]):
                self.log.error("Parser", "Error in parsing dir name slot ", str(slots))
                return CONST.invalid
            elif 'value' in slots[CONST.relativeDirNameSlot]:
                return self._parseRelativeDirNameSlot(slots[CONST.relativeDirNameSlot]['value'], requestId)
            elif 'value' in slots[CONST.dirNameSlot]:
                return self._parseDirNameSlot(slots[CONST.dirNameSlot]['value'], requestId)

        else:
            self.log.error("Parser", "Not expected slot type ", str(slots))
            return CONST.invalid

    def _parseRelativeDirNameSlot(self, utterances, requestId):
        if ('up' not in utterances):
            self.userFedbackProvider.send(msg="To change directory relatively, use word up", requestId=requestId)
            return CONST.invalid

        numberOfLevels = self._text2int(utterances)

        cmd = ''
        for x in range(0, numberOfLevels):
                cmd += '../'

        return [ChangeDirCmd(cmd, requestId), self._createPwdCmd(requestId)]

    def _text2int(self, utterances):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        for u in utterances.split():
            try:
                return int(locale.atof(u))
            except ValueError:
                self.log.debug("Parser", "cant parse as number ", u)

    def _parseDirNameSlot(self, utterances, requestId):
        return [ChangeDirCmd(userInput, requestId), self._createPwdCmd(requestId)]

    def _createPwdCmd(self, requestId):
        return RawCmd('pwd', requestId)

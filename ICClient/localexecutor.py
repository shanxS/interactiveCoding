from userinterface.printer import Printer
from userinterface.comms import VoiceRequestPuller, VoiceResponsePusher
from userinterface.userfeedbackprovider import UserFeedbackProvider
from utils.const import *
from utils.cmdtypes import *
import sys
import configparser
from subprocess import call
import os

"""
This layer actually executes the cmds. By the time req. reaches here
it is in form that it can be executed without further inferences from
end user's utterances.
"""


class LocalExecutor:
    def __init__(self, userFedbackProvider, logger):
        self.log = logger
        self.userFedbackProvider = userFedbackProvider

    def execute(self, perceivedCmd):
        if perceivedCmd == CONST.invalid:
            self.log.print(log="LocalExecutor", cmd="no perceived cmd", result="")

        elif perceivedCmd == CONST.end_session:
            self.log.print(log="LocalExecutor", cmd="End session request", result="")
            sys.exit()

        elif type(perceivedCmd) is RawCmd:
            cmd = perceivedCmd.getCmd()
            requestId = perceivedCmd.getRequestId()
            self.log.print(log="Perceived cmd is raw ", cmd=cmd, result="")
            self._execute(cmd, requestId)

        elif type(perceivedCmd) is SetProjectNameCmd:
            name = perceivedCmd.getName()
            requestId = perceivedCmd.getRequestId()
            self.log.print(log="Perceived cmd is", cmd="set project", result=name)
            self._setProject(name, requestId)

        elif type(perceivedCmd) is ChangeDirCmd:
            self._setPath(perceivedCmd.getPath(), requestId)

        elif type(perceivedCmd) is list:
            for cmd in perceivedCmd:
                self.execute(cmd)

    def _execute(self, cmd, requestId):
        try:
            retValue = call(cmd.split())
            if retValue != 0:
                self.userFedbackProvider.send(msg="Cmd exited with non zero return value " + cmd, requestId=requestId)
        except:  # not a good practice to have empty exception?
            self.userFedbackProvider.send(msg="Error executing cmd " + cmd, requestId=requestId)

    def _getAvailableProjects(self):
        config = configparser.ConfigParser()
        config.read('configs/projects.config')

        projects = {}
        for name in config.sections():
            projects[name.upper()] = config[name]['path']

        return projects

    def _setProject(self, potentialName, requestId):
        availableProjects = self._getAvailableProjects()
        self.log.debug("available projects", str(availableProjects), "")

        if potentialName.upper() in availableProjects:
            self._setPath(availableProjects[potentialName.upper()], requestId)
        else:
            self.userFedbackProvider.send(msg="Cant find project name in available projects", requestId=requestId)

    def _setPath(self, path, requestId):
        try:
            os.chdir(path)
        except FileNotFoundError:
            self.userFedbackProvider.send(msg="Path does not exist " + path, requestId=requestId)

class ChangeDirCmd:
    def __init__(self, dir, requestId):
        self.dir = dir
        self.requestId = requestId

    def getDir(self):
        return self.cmd

    def getRequestId(self):
        return self.requestId


class RawCmd:
    def __init__(self, cmd, requestId):
        self.cmd = cmd
        self.requestId = requestId

    def getCmd(self):
        return self.cmd

    def getRequestId(self):
        return self.requestId


class SetProjectNameCmd:
    def __init__(self, name, requestId):
        self.name = name
        self.requestId = requestId

    def getName(self):
        return self.name

    def getRequestId(self):
        return self.requestId

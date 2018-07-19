from colorama import Fore, Back, Style


class Printer:
    def __init__(self, isDebugMode):
        self.isDebugMode = isDebugMode

    def print(self, log, cmd, result):
        print('=> ' + log + ' ' + Fore.GREEN + cmd + ' ' + Style.RESET_ALL)
        print(result)

    def debug(self, log, cmd, result):
        if(self.isDebugMode):
            print('=> [DEBUG] ' + log + ' ' + Fore.LIGHTGREEN_EX + cmd + ' ' + Style.RESET_ALL)
            print(result)

    def error(self, log, cmd, result):
        print('=> [ERROR] ' + log + ' ' + Fore.LIGHTRED_EX + cmd + ' ' + Style.RESET_ALL)
        print(result)

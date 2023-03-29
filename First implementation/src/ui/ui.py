
class UI:

    def __init__(self):
        self.__commands = []

    def append_command(self, command):
        self.__commands.append(command)

    @property
    def commands(self):
        return self.__commands


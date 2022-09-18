import abc


class BaseCommand(abc.ABC):
    """
    The base class which represents a general interface of business-logic
    unit of the project - command.
    """

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        """
        It is an entry point to execute a command. Use this and only this
        method to invoke your command.
        """

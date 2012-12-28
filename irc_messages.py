class BaseMessage():
    """
    Base class for all irc messages which interact with server
    """
    def get_command(self):
        """ Function which returns string which can be sent to server """
        raise RuntimeError("Subclass need to override this function")

class PrivateMessage(BaseMessage):
    """
    PRIVMSG message.

    Example from irc server:
    :Waltsu!test@example.com PRIVMSG #testserver :hello world

    Example to irc server:
    PRIVMSG #testserver :Waltsu said: hello world
    """

    def __init__(self, channel, message):
        self._channel = channel
        self._message = message

    def get_command(self):
        return "PRIVMSG {channel} :{message}".format(channel = self._channel, message = self._message)

class PongMessage(BaseMessage):
    def __init__(self, ping_id):
        self._ping_id = ping_id

    def get_command(self):
        return "PONG :{ping_id}".format(ping_id = self._ping_id)

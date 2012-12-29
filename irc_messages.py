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
    """
    PONG mesage

    Example to server:
    PONG :12345
    """
    def __init__(self, ping_id):
        self._ping_id = ping_id

    def get_command(self):
        return "PONG :{ping_id}".format(ping_id = self._ping_id)

class JoinMessage(BaseMessage):
    """
    JOIN message

    Example from server:
    :Waltsu!waltsu@example.com JOIN #testserver

    Example to server:
    JOIN #testserver

    """
    def __init__(self, channel, nick = None):
        self._channel = channel
        self._nick = nick

    def get_command(self):
        return "JOIN {channel}".format(channel=self._channel)

class ModeMessage(BaseMessage):
    """
    MODE message

    Example from server: (Waltsu gave +o to yaib)
    :Waltsu!waltsu@example.com MODE #testserver +o yaib

    Example to server: (Give +o to waltsu)
    MODE #testserver +o Waltsu
    """
    def __init__(self, channel, flag, target = None):
        self._channel = channel
        self._flag = flag
        self._target = target

    def get_command(self):
        command = 'MODE {channel} {flag}'.format(channel=self._channel, flag=self._flag)
        if self._target:
            command += ' {target}'.format(target=self._target)
        return command

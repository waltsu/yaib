# -*- coding: utf8 -*-
import logging
logging.basicConfig()
logger = logging.getLogger('ircbot')
logger.setLevel(logging.DEBUG)

class IrcEvent():
    """
    Class which handles communication between scripting modules and ircbot.
    This class will be created with the information from message which fired this event.
    IrcBot inspects the instance of this class to find out information what the script wants to do with server.

    Class variables:
        to_server: data which will be sent to server. You can interact with ircserver with this variable.
    """

    def __init__(self, message):
        self.to_server = None

        self._server_message = message

    def send_to_channel(self, message_to_channel, channel = None):
        """
        Sets to_server variable so, that ircbot sends message_to_channel to channel. If channel isn't set, message will be sent to the same channel 
        """
        try:
            channel = getattr(self._server_message, 'channel')
            current_channel = self._server_message['channel']
        except AttributeError:
            logger.error("For some reason, server message didn't contain channel where to send the message")
        

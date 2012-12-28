# -*- coding: utf8 -*-
import logging
logging.basicConfig()
logger = logging.getLogger('ircbot')
logger.setLevel(logging.DEBUG)

class IrcEvent():
    """
    Class which contains information of current event.
    This class will be created with the information from message which fired this event.
    IrcBot inspects this event to find out information what the script wants to do with server.

    Class variables:
        to_server: list which contains messages to be sent to server
        info: Info to caller

        content: Content of the message that caused this event
        type: Type of the message that caused this event
        channel: Channel of the message that caused this event
        server: Server of the message that caused this event
    """

    def __init__(self, message):
        self.to_server = []
        self.info = None
        self._server_message = message

        self.content = message['content'] if message.has_key('content') else None
        self.type = message['type'] if message.has_key('type') else None
        self.channel = message['channel'] if message.has_key('channel') else None
        self.server = message['server'] if message.has_key('server') else None

    def send_to_channel(self, message_to_channel, channel = None):
        """
        Adds message_to_channel to 'to_server' list. 
        If channel isn't set, same channel is used that caused this event
        """
        current_channel = channel if channel else self.channel
        if current_channel:
            self.to_server.append("PRIVMSG {channel} :{message}".format(channel = current_channel, message = message_to_channel))
        else:
            logger.error("For some reason, server message didn't contain channel where to send the message")
        

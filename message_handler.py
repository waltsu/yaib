# -*- coding: utf8 -*-
import logging
logging.basicConfig()
logger = logging.getLogger('ircbot')
logger.setLevel(logging.DEBUG)

import re

class UnknowInputException(Exception):
    pass

class MessageHandler():
    def __init__(self):
        self._handlers = {"notice auth": self.handle_notice,
                          "ping": self.handle_ping}

    def handle(self, raw_message):
        parsed_message = self.parse(raw_message)
        message = parsed_message['message'].lower()
        self._handlers[message](parsed_message['content'])
        

    def parse(self, message):
        """
        This might need some adjusting, when handling more complex messages. The regex and message-content pair might not be enough
        """
        logger.debug("Parsing message: {message}".format(message=message))
        pattern = re.compile('(.+)\s:(.*)')
        result = re.search(pattern, message)
        if result:
            parsed_message = dict()
            parsed_message['message'] = result.group(1)
            parsed_message['content'] = result.group(2)
            return parsed_message
        else:
            raise UnknowInputException

    # HANDLERS
    def handle_notice(self, message):
        pass

    def handle_ping(self, message):
        pass

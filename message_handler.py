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
        self._handlers = {'notice': self.handle_notice,
                          'ping': self.handle_ping,
                          'mode': self.handle_mode}

    def handle(self, raw_message):
        try:
            parsed_message = self.parse(raw_message)
            message = parsed_message['message'].lower()
            try:
                return self._handlers[message](parsed_message['content'])
            except KeyError:
                logger.info('{message} not implemented yet'.format(message=message))
        except UnknowInputException:
            logger.info('Got unknown input: {message}'.format(message=raw_message))
            return;

    def parse(self, message):
        """
        This might need some adjusting, when handling more complex messages. The regex and message-content pair might not be enough
        """
        logger.debug("Parsing message: {message}".format(message=message))
        if message.startswith(':'):
            pattern = re.compile(':.+?\s(.+?)\s(.+?)\s?(.*)')
        else:
            pattern = re.compile('(.+)\s:(.*)')

        result = re.search(pattern, message)
        if result:
            parsed_message = dict()
            parsed_message['message'] = result.group(1)
            if len(result.groups()) == 3:
                parsed_message['channel'] = result.group(2)
                parsed_message['content'] = result.group(3)
            else:
                parsed_message['content'] = result.group(2)

            return parsed_message
        else:
            raise UnknowInputException

    # HANDLERS
    def handle_notice(self, message):
        logger.info("Got notice {notice}".format(notice=message))

    def handle_ping(self, message):
        return 'PONG :{ping}'.format(ping=message)

    def handle_mode(self, message):
        pass

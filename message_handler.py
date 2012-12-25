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
                          'mode': self.handle_mode,
                          '376': self.handle_end_of_motd}

    """
    Return value of this function must be either None or dictionary with action and data attributes.

    Action types:
    to_server => send data to server
    logged_in => message that indicates that service has accept our login attempt
    """
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
        return_data = {}
        return_data['data'] = 'PONG :{ping}'.format(ping=message)
        return_data['action'] = 'to_server'
        return return_data

    def handle_mode(self, message):
        pass

    def handle_end_of_motd(self, message):
        return {'action': 'logged_in', 'data': ''}

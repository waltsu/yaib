# -*- coding: utf8 -*-
import logging
logging.basicConfig()
logger = logging.getLogger('ircbot')
logger.setLevel(logging.DEBUG)

import re
import settings

class UnknowInputException(Exception):
    pass

class MessageHandler():
    def __init__(self):
        self._handlers = {'notice': self._handle_notice,
                          'ping': self._handle_ping,
                          'mode': self._handle_mode,
                          'privmsg': self._handle_priv_msg,
                          '376': self._handle_end_of_motd,
                          '433': self._handle_nickname_already_in_use}

        self._script_modules = []
        for module in settings.SCRIPT_MODULES:
            self._script_modules.append(__import__(module,fromlist=['']))
            

    """
    Return value of this function must be either None or dictionary with action and data attributes.

    Action types:
    to_server => send data to server
    logged_in => message that indicates that service has accept our login attempt
    nickname_already_in_use => Bot tried to login with the nickname that was already in us
    """
    def handle(self, raw_message):
        try:
            parsed_message = self.parse(raw_message)
            message = parsed_message['type'].lower()
            try:
                return self._handlers[message](parsed_message)
            except KeyError:
                logger.info('{message} not implemented yet'.format(message=message))
        except UnknowInputException:
            logger.info('Got unknown input: {message}'.format(message=raw_message))
            return;

    def parse(self, message):
        logger.debug("Parsing message: {message}".format(message=message))
        if message.startswith(':'):
            pattern = re.compile(':(.+?)\s(.+?)\s(.+?)\s(.*)')
        else:
            pattern = re.compile('(.+)\s:(.*)')

        result = re.search(pattern, message)
        if result:
            parsed_message = dict()
            if len(result.groups()) == 4:
                parsed_message['server'] = result.group(1)
                parsed_message['type'] = result.group(2)
                parsed_message['channel'] = result.group(3)
                parsed_message['content'] = result.group(4)
            else:
                parsed_message['type'] = result.group(1)
                parsed_message['content'] = result.group(2)

            return parsed_message
        else:
            raise UnknowInputException

    # HANDLERS
    def _handle_notice(self, message):
        logger.info("Got notice {notice}".format(notice=message['content']))

    def _handle_ping(self, message):
        return_data = {}
        return_data['data'] = 'PONG :{ping}'.format(ping=message['content'])
        return_data['action'] = 'to_server'
        return return_data

    def _handle_mode(self, message):
        pass

    def _handle_end_of_motd(self, message):
        return {'action': 'logged_in', 'data': ''}

    def _handle_priv_msg(self, message):
        logger.info("Got priv {msg}".format(msg=message))

    def _handle_nickname_already_in_use(self, message):
        return {'action': 'nickname_already_in_use', 'data': ''}

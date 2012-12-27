# -*- coding: utf8 -*-
import logging
logging.basicConfig()
logger = logging.getLogger('ircbot')
logger.setLevel(logging.DEBUG)

import re
import settings

from irc_event import IrcEvent

class UnknowInputException(Exception):
    pass

class MessageHandler():
    """
    Class that handles messages from ircbot
    """
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
            

    def handle(self, raw_message):
        """
        Function that handles incoming message. The return value of this function is either None or dictionary with action and data attributes. Action tells to caller what to do with data.

        Current action types:
        to_server: send data-attribute to server
        info: Something happened that caller might want to know
        """
        try:
            parsed_message = self._parse(raw_message)
            event = IrcEvent(parsed_message)
            type = event.type.lower()
            try:
                return self._handlers[type](parsed_message)
            except KeyError:
                logger.info('{message} not implemented yet'.format(message=message))
        except UnknowInputException:
            logger.info('Got unknown input: {message}'.format(message=raw_message))
            return;

    def _parse(self, message):
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

    def _call_script_modules(self, func, **kwargs):
        for module in self._script_modules:
            try:
                callable_function = getattr(module,func)
                if callable(callable_function):
                    try:
                        callable_function(**kwargs)
                    except Exception as e:
                        logger.error("Script {module} raised error: {error}".format(module=module, error=e))
                else:
                    logger.debug("Script module {module} {function} isn't callable".format(module=module, function=func))
            except AttributeError:
                logger.debug("Script module {module} doesn't have method {function}".format(module=module, function=func))

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
        return {'action': 'info', 'data': 'logged_in'}

    def _handle_priv_msg(self, message):
        script_message = {'content': message['content'].strip()[1:], # Excluding the first ':' character
                          'nick': message['server'].split('!')[0],
                          'channel': message['channel']}
        
        logger.info("Got priv {msg}".format(msg=message))
        self._call_script_modules('on_priv_message', message=script_message)

    def _handle_nickname_already_in_use(self, message):
        return {'action': 'info', 'data': 'nickname_already_in_use'}

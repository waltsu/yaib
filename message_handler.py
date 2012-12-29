# -*- coding: utf8 -*-
import logging
logging.basicConfig()
logger = logging.getLogger('ircbot')
logger.setLevel(logging.DEBUG)

import re
import settings

from irc_event import IrcEvent
from irc_messages import *

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
                          'join': self._handle_join,
                          'part': self._handle_part,
                          'topic': self._handle_topic,
                          '376': self._handle_end_of_motd,
                          '433': self._handle_nickname_already_in_use}

        self._script_modules = []
        self._event = None

        for module in settings.SCRIPT_MODULES:
            self._script_modules.append(__import__(module,fromlist=['']))

    def handle(self, raw_message):
        """
        Function that handles incoming message. The return value is IrcEvent instance which is modified by handlers. Handlers has modified the event so that caller should know what to do
        """
        try:
            parsed_message = self._parse(raw_message)
            self._event = IrcEvent(parsed_message)
            type = self._event.type.lower()
            try:
                self._handlers[type]()
                return self._event
            except KeyError:
                logger.info('{message} not implemented yet'.format(message=self._event.type))
        except UnknowInputException:
            logger.info('Got unknown input: {message}'.format(message=raw_message))
            return;

    def _parse(self, message):
        """
        Parses raw message to dictionary.
        """
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
                parsed_message['target'] = result.group(3)
                parsed_message['content'] = result.group(4)
            else:
                parsed_message['type'] = result.group(1)
                parsed_message['content'] = result.group(2)

            return parsed_message
        else:
            raise UnknowInputException

    def _call_script_modules(self, func, **kwargs):
        """
        Calls 'func'-function from every script_module if possible. The first parameter of function call is self._event and other parameters are passed from **kwargs.
        Example:
        If this function is called with:

            _call_script_modules('on_join', nick='nick', channel='#channel')

        Then on_join function of every script_module will be called with:
            script_module.on_join(self._event, nick='nick', channel='#channel')

        So scriptmodule should have following function:
            def on_join(event, nick, channel):
                pass

        If module doesn't have the function (which is highly possible and expected), error will be logged to logger.debug
        """
        for module in self._script_modules:
            try:
                callable_function = getattr(module,func)
                if callable(callable_function):
                    try:
                        callable_function(self._event, **kwargs)
                    except Exception as e:
                        logger.error("Script {module} raised error: {error}".format(module=module, error=e))
                else:
                    logger.debug("Script module {module} {function} isn't callable".format(module=module, function=func))
            except AttributeError:
                logger.debug("Script module {module} doesn't have method {function}".format(module=module, function=func))

    # HANDLERS
    def _handle_notice(self):
        logger.info("Got notice {notice}".format(notice=self._event.content))

    def _handle_ping(self):
        self._event.to_server.append(PongMessage(self._event.content))

    def _handle_mode(self):
        pass

    def _handle_end_of_motd(self):
        for channel in settings.CHANNELS:
            self._event.to_server.append(JoinMessage(channel))

    def _handle_priv_msg(self):
        script_message = {'content': self._event.content.strip()[1:], # Excluding the first ':' character
                          'nick': self._event.server.split('!')[0],
                          'target': self._event.target}

        self._call_script_modules('on_priv_message', message=script_message)

    def _handle_join(self):
        script_message = {'nick': self._event.server.split('!')[0],
                          'channel': self._event.target}
        self._call_script_modules('on_join', message=script_message)

    def _handle_part(self):
        script_message = {'nick': self._event.server.split('!')[0],
                          'channel': self._event.target}
        self._call_script_modules('on_part', message=script_message)

    def _handle_topic(self):
        logger.debug("Topic changed")

    def _handle_nickname_already_in_use(self):
        logger.error('Nickname already in use')
        raise RuntimeError('Nickname already in use')

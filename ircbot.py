# -*- coding: utf8 -*-
import settings

import sys
import socket
import threading
import functools
from message_handler import MessageHandler

import logging
logging.basicConfig()
logger = logging.getLogger('ircbot')
logger.setLevel(logging.DEBUG)

class IrcBot:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port, ircname):
        """ Function thats connects bot to irc server """
        def login_to_server():
            logger.info("Logging to server with username: {user}".format(user=self._ircname))
            self._send_to_server("NICK {nick}".format(nick=self._ircname))
            self._send_to_server("USER {nick} 8 * : Yet another Ircbot".format(nick=self._ircname))

        logger.info("setting bot's ircname to {ircname}".format(ircname=ircname))
        self._ircname = ircname
        logger.info("connecting to %s:%s" % (host, port))
        self._socket.connect((host, port))
        logger.info("connected")

        login_to_server()

        self._response_loop()

    def _response_loop(self):
        def get_server_response():
            response = ''
            while '\r\n' not in response:
                response += self._socket.recv(1)

            return response

        while True:
            server_response = get_server_response()
            handle_thread = threading.Thread(target=functools.partial(self._handle_server_response, server_response))
            handle_thread.start()

    def _send_to_server(self, data):
        self._socket.sendall(data + '\r\n')
        logger.debug("Sent data: {data}".format(data=data))

    def _handle_server_response(self, response):
        def react_info(data):
            if data is 'logged_in':
                # Join to servers
                for channel in settings.CHANNELS:
                    self._send_to_server("JOIN {channel}".format(channel=channel))
            elif data is 'nickname_already_in_use':
                logger.error('Nickname already in use')
                raise RuntimeError('Nickname already in use')

        def react_to_server(data):
            self._send_to_server(response['data'])

        message_handler = MessageHandler()
        response = message_handler.handle(response)
        if response:
            if response['action'] is 'to_server':
                react_to_server(response['data'])
            if response['action'] is 'info':
                react_info(response['data']) 
if __name__ == '__main__':
    ircbot = IrcBot()
    try:
        host = getattr(settings, 'SERVER')
        port = int(getattr(settings, 'PORT'))
        ircname = getattr(settings, 'IRCNAME')

        ircbot.connect(host, port, ircname)
    except AttributeError:
        logger.error('SERVER NOT CONFIGURED!')
        sys.exit()

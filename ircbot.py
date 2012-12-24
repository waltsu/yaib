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
        logger.info("setting bot's ircname to {ircname}".format(ircname=ircname))
        self._ircname = ircname
        logger.info("connecting to %s:%s" % (host, port))
        self._socket.connect((host, port))
        logger.info("connected")
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

    def _handle_server_response(self, response):
        message_handler = MessageHandler()
        message_handler.handle(response)


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

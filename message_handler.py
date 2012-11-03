import logging
logging.basicConfig()
logger = logging.getLogger('ircbot')
logger.setLevel(logging.DEBUG)

class MessageHandler():
    def handle(self, message):
        logger.debug("Got response: %s" % message)

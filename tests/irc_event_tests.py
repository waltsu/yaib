import unittest

from yaib.irc_event import IrcEvent

class IrcEventTests(unittest.TestCase):
    
    def setUp(self):
        test_message = {'content': 'hello world', 'nick': 'Waltsu', 'channel': '#testserver'}
        self.event = IrcEvent(test_message)

    def test_ircflow_initialization(self):
        self.assertEquals(self.event._server_message['channel'], '#testserver')

    def test_send_to_channel(self):
        self.event.send_to_channel("Hello world") 
        #self.assertEquals(self.event.to_server, "PRIVMSG #testserver :Hello world")

import unittest

from yaib.irc_event import IrcEvent
from yaib.irc_messages import PrivateMessage

class IrcEventTests(unittest.TestCase):
    
    def setUp(self):
        test_message = {'content': 'hello world', 'type': 'PRIVMSG', 'target': '#testserver', 'server': 'Waltsu!waltsu@waltsu.fi'}
        self.event = IrcEvent(test_message)

    def test_ircevent_initialization(self):
        self.assertEquals(self.event._server_message['target'], '#testserver')


import unittest

from yaib.irc_event import IrcEvent

class IrcEventTests(unittest.TestCase):
    
    def setUp(self):
        test_message = {'content': 'hello world', 'type': 'PRIVMSG', 'target': '#testserver', 'server': 'Waltsu!waltsu@waltsu.fi'}
        self.event = IrcEvent(test_message)

    def test_ircevent_initialization(self):
        self.assertEquals(self.event._server_message['target'], '#testserver')

    def test_send_to_channel(self):
        self.event.send_to_channel("Hello world") 
        self.assertEquals(self.event.to_server, ["PRIVMSG #testserver :Hello world"])

        self.event.send_to_channel("Hello world", "#other_channel")
        self.assertEquals(self.event.to_server, ["PRIVMSG #testserver :Hello world", "PRIVMSG #other_channel :Hello world"])

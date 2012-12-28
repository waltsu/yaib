import unittest

from yaib.irc_messages import PrivateMessage, PongMessage

class IrcMessagesTests(unittest.TestCase):

    def test_private_message(self):
        private_message = PrivateMessage('#channel', 'some message')
        self.assertEquals(private_message.get_command(), 'PRIVMSG #channel :some message')

    def test_pong_message(self):
        pong_message = PongMessage(1234)
        self.assertEquals(pong_message.get_command(), 'PONG :1234')

import unittest

from yaib.irc_messages import PrivateMessage

class IrcMessagesTests(unittest.TestCase):

    def test_private_message(self):
        private_message = PrivateMessage('#channel', 'some message')
        self.assertEquals(private_message.get_command(), 'PRIVMSG #channel :some message')

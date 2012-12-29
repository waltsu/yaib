import unittest

from yaib.irc_messages import *

class IrcMessagesTests(unittest.TestCase):

    def test_private_message(self):
        private_message = PrivateMessage('#channel', 'some message')
        self.assertEquals(private_message.get_command(), 'PRIVMSG #channel :some message')

    def test_pong_message(self):
        pong_message = PongMessage(1234)
        self.assertEquals(pong_message.get_command(), 'PONG :1234')

    def test_join_message(self):
       join_message = JoinMessage('#channel')
       self.assertEquals(join_message.get_command(), 'JOIN #channel')

    def test_mode_message(self):
        mode_message = ModeMessage('#channel', '+i')
        self.assertEquals(mode_message.get_command(), 'MODE #channel +i')

        mode_message_with_target = ModeMessage('#channel', '+o', 'yaib')
        self.assertEquals(mode_message_with_target.get_command(), 'MODE #channel +o yaib')

    def test_topic_message(self):
        topic_message = TopicMessage('#channel')
        self.assertEquals(topic_message.get_command(), 'TOPIC #channel')

        topic_message_with_message = TopicMessage('#channel', 'another topic')
        self.assertEquals(topic_message_with_message.get_command(), 'TOPIC #channel :another topic')

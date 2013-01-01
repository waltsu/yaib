import unittest

from mock import patch

from yaib.message_handler import MessageHandler
from yaib.irc_event import IrcEvent
from irc_messages import PongMessage

from tests.fixtures import script

class MessageHandlerTests(unittest.TestCase):
    PART_MESSAGE = ':Waltsu!waltsu@example.com PART #secondtest '
    @patch.object(MessageHandler, "_handle_notice")
    def test_notice_parsing(self, m_notice):
        handler = MessageHandler()
        test_message = ':servercentral.il.us.quakenet.org NOTICE yaib :on 1 ca 1(4) ft 20(20)'
        handler.handle(test_message)
        self.assertTrue(m_notice.called)

    def test_ping_parsing(self):
        handler = MessageHandler()
        test_message = 'PING :687010916'
        event = handler.handle(test_message)
        self.assertEqual(event.to_server[0].get_command(), PongMessage(687010916).get_command())

    @patch.object(MessageHandler, '_handle_mode')
    def test_message_without_content(self, m_mode):
        test_message = ':yaib!~yaib@a91-155-146-6.elisa-laajakaista.fi MODE yaib +i'
        handler = MessageHandler()
        response = handler.handle(test_message)
        self.assertTrue(m_mode.called)

    def test_end_of_motd(self):
        test_message = ':servercentral.il.us.quakenet.org 376 yaib :End of /MOTD command.'
        handler = MessageHandler()
        event = handler.handle(test_message)
        self.assertEquals(event.to_server[0].get_command(), "JOIN #testserver")

    @patch.object(MessageHandler, '_handle_priv_msg')
    def test_privmsg(self, m_priv_msg):
        test_message = ':Waltsu!waltsu@example.com PRIVMSG #testserver :uujee'
        handler = MessageHandler()
        response = handler.handle(test_message)
        self.assertTrue(m_priv_msg.called)

    def test_nickname_already_in_use(self):
        test_message = ':servercentral.il.us.quakenet.org 433 * Waltsu :Nickname is already in use.'
        handler = MessageHandler()
        self.assertRaises(RuntimeError, handler.handle, test_message)

    @patch.object(script, 'on_join')
    def test_on_join(self, m_on_join):
        handler = MessageHandler()
        handler.add_script_module("tests.fixtures.script")

        test_message = ':Waltsu!waltsu@example.com JOIN #secondtest '
        event = handler.handle(test_message)

        self.assertTrue(m_on_join.called)

    @patch.object(script, 'on_part')
    def test_on_part(self, m_on_part):
        handler = MessageHandler()
        handler.add_script_module("tests.fixtures.script")

        event = handler.handle(self.PART_MESSAGE)

        self.assertTrue(m_on_part.called)

    @patch.object(script, 'on_priv_message')
    def test_script_calling(self, m_on_priv_message):
        handler = MessageHandler()
        handler.add_script_module("tests.fixtures.script")

        mock_event = IrcEvent({'content': 'some content', 'channel': '#channel', 'type': 'privmsg'})
        handler._event = mock_event
        handler._call_script_modules('on_priv_message', message="some message")

        m_on_priv_message.assert_called_with(mock_event, message="some message")

    @patch.object(MessageHandler, '_handle_topic')
    def test_on_topic(self, m_handle_topic):
        test_message = ':Waltsu!waltsu@example.com TOPIC #secondtest :a'
        handler = MessageHandler()
        event = handler.handle(test_message)
        self.assertTrue(m_handle_topic.called)

    @patch.object(script, 'on_part')
    def test_script_error_handling(self, m_on_part):
        m_on_part.side_effect = Exception("Should not bubble from handler")

        handler = MessageHandler()
        handler.add_script_module("tests.fixtures.script")

        event = handler.handle(self.PART_MESSAGE)
        self.assertTrue(m_on_part.called)

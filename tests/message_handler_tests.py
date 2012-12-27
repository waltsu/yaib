import unittest

from mock import patch

from yaib.message_handler import MessageHandler

from scripts import test_script

class MessageHandlerTests(unittest.TestCase):
    @patch.object(MessageHandler, "_handle_notice")
    def test_notice_parsing(self, m_notice):
        handler = MessageHandler()
        test_message = ':servercentral.il.us.quakenet.org NOTICE yaib :on 1 ca 1(4) ft 20(20)'
        handler.handle(test_message)
        self.assertTrue(m_notice.called)

    def test_ping_parsing(self):
        handler = MessageHandler()
        test_message = 'PING :687010916'
        response = handler.handle(test_message)
        self.assertEqual(response['data'], 'PONG :687010916')

    @patch.object(MessageHandler, '_handle_mode')
    def test_message_without_content(self, m_mode):
        test_message = ':yaib!~yaib@a91-155-146-6.elisa-laajakaista.fi MODE yaib +i'
        handler = MessageHandler()
        response = handler.handle(test_message)
        self.assertTrue(m_mode.called)

    def test_end_of_motd(self):
        test_message = ':servercentral.il.us.quakenet.org 376 yaib :End of /MOTD command.'
        handler = MessageHandler()
        response = handler.handle(test_message)
        self.assertEquals(response['data'], 'logged_in')

    @patch.object(MessageHandler, '_handle_priv_msg')
    def test_privmsg(self, m_priv_msg):
        test_message = ':Waltsu!vavirta@linux.utu.fi PRIVMSG #testserver :uujee'
        handler = MessageHandler()
        response = handler.handle(test_message)
        self.assertTrue(m_priv_msg.called)

    def test_nickname_already_in_use(self):
        test_message = ':servercentral.il.us.quakenet.org 433 * Waltsu :Nickname is already in use.'
        handler = MessageHandler()
        response = handler.handle(test_message)
        self.assertEquals(response['data'], 'nickname_already_in_use')

    @patch.object(test_script, 'on_priv_message')
    def test_script_calling(self, m_on_priv_message):
        handler = MessageHandler()
        handler._call_script_modules('on_priv_message', message="some message")
        m_on_priv_message.assert_called_with(message="some message")

    def test_script_error_handling(self):
        handler = MessageHandler()
        # If not handled correctly, raise_error will raise exception
        handler._call_script_modules('raise_error', message="some message")


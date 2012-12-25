import unittest

from mock import patch

from yaib.message_handler import MessageHandler

class MessageHandlerTests(unittest.TestCase):
    @patch.object(MessageHandler, "handle_notice")
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

    @patch.object(MessageHandler, 'handle_mode')
    def test_message_without_content(self, m_mode):
        test_message = ':yaib!~yaib@a91-155-146-6.elisa-laajakaista.fi MODE yaib +i'
        handler = MessageHandler()
        response = handler.handle(test_message)
        self.assertTrue(m_mode.called)

    def test_end_of_motd(self):
        test_message = ':servercentral.il.us.quakenet.org 376 yaib :End of /MOTD command.'
        handler = MessageHandler()
        response = handler.handle(test_message)
        self.assertEquals(response['action'], 'logged_in')

    @patch.object(MessageHandler, 'handle_priv_msg')
    def test_privmsg(self, m_priv_msg):
        test_message = ':Waltsu!vavirta@linux.utu.fi PRIVMSG #testserver :uujee'
        handler = MessageHandler()
        response = handler.handle(test_message)
        self.assertTrue(m_priv_msg.called)


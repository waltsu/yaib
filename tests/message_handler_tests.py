import unittest

from mock import patch

from yaib.message_handler import MessageHandler

class MessageHandlerTests(unittest.TestCase):
    @patch.object(MessageHandler, "handle_notice")
    def test_notice_parsing(self, m_notice):
        handler = MessageHandler()
        test_message = 'NOTICE AUTH :*** Looking up your hostname'
        handler.handle(test_message)
        self.assertTrue(m_notice.called)

    @patch.object(MessageHandler, "handle_ping")
    def test_ping_parsing(self, m_ping):
        handler = MessageHandler()
        test_message = 'PING :687010916'
        handler.handle(test_message)
        self.assertTrue(m_ping.called)

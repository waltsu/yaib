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


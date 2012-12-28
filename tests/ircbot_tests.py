import unittest
from socket import socket

from mock import patch
from mock import call

from ircbot import IrcBot
from message_handler import MessageHandler
from irc_event import IrcEvent

class IrcbotTest(unittest.TestCase):

    def setUp(self):
        self._ircbot = IrcBot()

    @patch.object(socket, 'connect')
    @patch.object(socket, 'sendall') 
    @patch.object(IrcBot, '_response_loop') 
    def test_connecting(self, m_response_loop, m_sendall, m_connect):
        self.assertTrue(self._ircbot != None)
        self._ircbot.connect('host', '6667', 'mynick')
        self.assertTrue(m_connect.called)
        self.assertTrue(m_response_loop.called)

    @patch.object(socket, 'sendall')
    def test_send_to_server(self, m_sendall):
        self._ircbot._send_to_server('something to server')

        m_sendall.assert_called_with('something to server\r\n')

    @patch.object(IrcBot, '_send_to_server') 
    @patch.object(MessageHandler, 'handle')
    def test_to_server_handling(self, m_handle, m_send_to_server):
        def handle_se(response):
           event = IrcEvent({})
           event.to_server = ["Something to server", "Something more"]
           return event
           
        m_handle.side_effect = handle_se
        self._ircbot._handle_server_response("")
        call_args = m_send_to_server.mock_calls
        self.assertTrue(call('Something to server') in call_args) 
        self.assertTrue(call('Something more') in call_args) 


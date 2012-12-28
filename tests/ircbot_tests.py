import unittest
from ircbot import IrcBot

class IrcbotTest(unittest.TestCase):

    def setUp(self):
        self._ircbot = IrcBot()

    def test_connecting(self):
        assertIsNotNone(self._ircbot)

import settings

from irc_messages import PrivateMessage

def on_priv_message(event, message):
    msg_to_server = "{user} said: {content}".format(user=message['nick'], content=message['content'])
    print "Repeating the message."

    # If user sends private message to the bot, target is our bot
    # We want to answer back to the nick, not to us
    if message['target'] == settings.IRCNAME:
        event.to_server.append(PrivateMessage(message['nick'], msg_to_server))
    else:
        event.to_server.append(PrivateMessage(message['target'], msg_to_server))

def on_join(event, message):
    event.to_server.append(PrivateMessage(message['target'], "{nick} joined to channel".format(nick=message['nick'])))
    event.to_server.append(PrivateMessage(message['target'], "Hello {nick}!".format(nick=message['nick'])))

def on_part(event, message):
    print "on part: {message}".format(message=message)

def raise_error(event, message):
    """
    Function for testing error handling on script system
    """
    print "Raising type error"
    raise TypeError("Caller should handle this!")

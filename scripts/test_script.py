import settings

def on_priv_message(event, message):
    msg_to_server = "{user} said: {content}".format(user=message['nick'], content=message['content'])
    print "Repeating the message."

    # If user sends privat message to the bot, target is our bot
    # We want to answer back to the nick, not to us
    if message['target'] == settings.IRCNAME:
        event.send_to_channel(msg_to_server, message['nick'])
    else:
        event.send_to_channel(msg_to_server)

def on_join(event, message):
    event.send_to_channel("{nick} joined to channel".format(nick=message['nick']))
    event.send_to_channel("Hello {nick}!".format(nick=message['nick']))

def on_part(event, message):
    print "on part: {message}".format(message=message)

def raise_error(event, message):
    """
    Function for testing error handling on script system
    """
    print "Raising type error"
    raise TypeError("Caller should handle this!")

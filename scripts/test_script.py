def on_priv_message(event, message):
    print "Repeating the message."
    msg_to_server = "{user} said: {content}".format(user=message['nick'], content=message['content'])
    event.send_to_channel(msg_to_server)

def on_join(event, message):
    print "on join: {message}".format(message=message)

def on_part(event, message):
    print "on part: {message}".format(message=message)

def raise_error(event, message):
    """
    Function for testing error handling on script system
    """
    print "Raising type error"
    raise TypeError("Caller should handle this!")

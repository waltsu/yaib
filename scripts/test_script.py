def on_priv_message(message):
    print "hello priv message: {message}".format(message=message)

def raise_error(message):
    """
    Function for testing error handling on script system
    """
    print "Raising type error"
    raise TypeError("Caller should handle this!")

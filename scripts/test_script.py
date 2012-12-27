def on_priv_message(message):
    print "hello priv message: {message}".format(message=message)

"""
Function for testing error handling on script system
"""
def raise_error(message):
    print "Raising type error"
    raise TypeError("Caller should handle this!")

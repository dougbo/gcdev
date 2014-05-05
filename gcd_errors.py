

class Fail(Exception):
    """
    Assertion failure. Something went very wrong.
    """
    pass

class InvalidCondition(Exception):
    """
    Invalid Condition: some mismatch of parameters or specifications gave
    us a condition we can't interpret
    """
    pass

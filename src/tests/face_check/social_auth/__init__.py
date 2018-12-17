class step(object):
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise exc_val

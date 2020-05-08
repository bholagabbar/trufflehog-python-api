"""
Contains the TrufflehogApiError which is the exception thrown at the API layer
"""


class TrufflehogApiError(Exception):
    """Wraps API specific errors and lower level exceptions thrown by library dependencies """

    def __init__(self, reason, response=None, api_code=None):
        self.reason = reason
        self.response = response
        self.api_code = api_code
        super(TrufflehogApiError, self).__init__(reason)

    def __str__(self):
        return self.reason

    def __repr__(self):
        return ('TrufflehogApiError(reason={0}, response={1}, api_code={2})'
                .format(str(self.reason), str(self.response), str(self.api_code)))

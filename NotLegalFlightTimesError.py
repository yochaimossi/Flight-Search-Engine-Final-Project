class NotLegalFlightTimesError(Exception):
    def __init__(self, msg="Landing time must be at least 1 minute after departure time"):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.msg}'
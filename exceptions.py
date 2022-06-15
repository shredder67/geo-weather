class CantGetCoordinates(Exception):
    """Program can't get current GPS coordinates"""
    def __init__(self):
        self.message = "Program can't get current GPS coordinates"
        super(CantGetCoordinates, self).__init__(self.message)

class ApiServiceError(Exception):
    """Program can't get current weather from API"""
    def __init__(self):
        self.message = "Program can't get current weather from API"
        super(ApiServiceError, self).__init__(self.message)
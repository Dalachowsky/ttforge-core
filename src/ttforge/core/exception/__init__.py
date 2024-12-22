
from .TTForgeException import TTForgeException

class DoesNotDepend(TTForgeException):
    def __init__(self, regID: str, depRegID: str) -> None:
        super().__init__(f"{regID} does not depend on {depRegID}")
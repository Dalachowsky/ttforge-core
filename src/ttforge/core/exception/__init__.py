
from .TTForgeException import TTForgeException

class DoesNotDepend(TTForgeException):
    def __init__(self, regID: str, depRegID: str) -> None:
        super().__init__(f"{regID} does not depend on {depRegID}")

class RegistrationError(TTForgeException):
    pass

class EntityDeserializationError(TTForgeException):
    pass

class DuplicateEntry(RegistrationError):
    def __init__(self, regID: str, msg: str = "") -> None:
        super().__init__(f"Entry with ID: {regID} already registered. {msg}")

class EntryNotFound(TTForgeException):
    def __init__(self, regID: str) -> None:
        super().__init__(f"ID {regID} not found")

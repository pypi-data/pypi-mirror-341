from enum import Enum

class Extra:
    @staticmethod
    def EnumsToValues(Enums: list[Enum]) -> list[any]:
        values = []
        for enum in Enums:
            values.append(enum.value)
        return values

    @staticmethod
    def MakeIter(obj: any) -> any:
        if not obj or hasattr(obj, "__iter__"):
            return obj
        return [obj]


class RateLimitException(Exception):
    def __init__(self):
        super().__init__("Retry later")

class FormatException(Exception):
    def __init__(self, message):
        super().__init__(message)

class NoMaterialException(Exception):
    def __init__(self, message='No material for moderation'):
        super().__init__(message)


class AfterValidationException(Exception):
    def __init__(self, message='Validation error'):
        super().__init__(message)


class NotUniqueException(Exception):
    def __init__(self, message='Material is not unique'):
        super().__init__(message)


class ClientS3exception(Exception):
    def __init__(self, message='Server connection error'):
        super().__init__(message)

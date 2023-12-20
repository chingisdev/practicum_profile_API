from fastapi import HTTPException, status


class CustomException(HTTPException):
    status_code: status

    def __init__(self, detail, headers=None) -> None:
        status_code = self.status_code
        super().__init__(status_code, detail, headers)


class KafkaException(CustomException):
    """Invalid Kafka."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class UserDataException(CustomException):
    """User data exception."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class OtherException(CustomException):
    """Other exception."""

    status_code = status.HTTP_506_VARIANT_ALSO_NEGOTIATES

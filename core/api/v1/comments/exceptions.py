from functools import wraps
from ninja.errors import HttpError
from pydantic import ValidationError
from core.apps.common.exceptions import ServiceException
from core.apps.customers.exceptions.customers import CustomerTokenInvalid
from core.apps.reviews.exceptions.comment import CommentNotFound, NoCommentsFound


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as error:
            raise HttpError(status_code=400, message="Invalid input: ")
        except CustomerTokenInvalid as error:
            raise HttpError(status_code=401, message=error.message)
        except PermissionError:
            raise HttpError(status_code=403, message="No access rights")
        except CommentNotFound as error:
            raise HttpError(status_code=404, message=error.message)
        except NoCommentsFound as error:
            raise HttpError(status_code=404, message=error.message)
        except ServiceException as error:
            raise HttpError(status_code=500, message=error.message)
        except Exception as error:
            raise HttpError(status_code=500, message="Internal Server Error")

    return wrapper

"""
These error extensions are used in the flask API endpoints to
return specific messages to the client.
When any of these exceptions are raised, the API will return a specific
error message and status code.

Note: for these to work without returning a 500 error, the specific
endpoint raising them must decorated with the handle_endpoint_exceptions
decorator from app/utils/helpers.py.
"""

class BadRequest(Exception): ...

class NotFound(Exception): ...

class InternalServerError(Exception): ...

class UnAuthenticated(Exception): ...

class UnAuthorized(Exception): ...
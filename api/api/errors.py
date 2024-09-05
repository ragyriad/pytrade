import traceback
from rest_framework import status

class AppError(Exception):
    def __init__(self, error_name, message, status_code, exc_traceback=None):
        self.error_name = error_name
        self.message = message
        self.status_code = status_code
        self.traceback = exc_traceback or traceback.format_exc()
        super().__init__(self.message)

    def __str__(self):
        return f"{self.error_name}: {self.message}"

class LoginError(AppError):
    error_name = "LoginError"
    message = "A Login Error has occurred"
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self):
        super().__init__(self.error_name, self.message, self.status_code)

class MethodInputError(AppError):
    error_name = "MethodInputError"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self, message):
        super().__init__(self.error_name, message.strip(), self.status_code)

class EmptyTokensError(AppError):
    error_name = "EmptyTokensError"
    message = "Tokens are empty"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self):
        super().__init__(self.error_name, self.message, self.status_code)

class InvalidAccessTokenError(AppError):
    error_name = "InvalidAccessTokenError"
    message = "An Invalid access token error was given, please try again"
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self):
        super().__init__(self.error_name, self.message, self.status_code)

class InvalidRefreshTokenError(AppError):
    error_name = "InvalidRefreshTokenError"
    message = "An Invalid refresh token error was given, please try again"
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self):
        super().__init__(self.error_name, self.message, self.status_code)

class OTPCallbackNone(AppError):
    error_name = "OTPCallbackNone"
    message = "An wealthsimple otp user account was triggered, please use a callback function"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self):
        super().__init__(self.error_name, self.message, self.status_code)

class WSOTPError(AppError):
    error_name = "WSOTPError"
    message = "Otp is null, try again with your authenticating method"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(self.error_name, self.message, self.status_code)

class WSOTPLoginError(AppError):
    error_name = "WSOTPLoginError"
    message = "A Wealthsimple otp login error happened, please try again"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(self.error_name, self.message, self.status_code)

class TSXStopLimitPriceError(AppError):
    error_name = "TSXStopLimitPriceError"
    message = "TSX/TSX-V securities must have an equivalent stop and limit price"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self):
        super().__init__(self.error_name, self.message, self.status_code)

class WealthsimpleServerError(AppError):
    error_name = "WealthsimpleServerError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message="Wealthsimple endpoint might be down: return a 5XX http code"):
        super().__init__(self.error_name, message, self.status_code)

class RouteNotFoundException(AppError):
    error_name = "RouteNotFoundException"
    message = "Wealthsimple endpoint not found: return a 404 http code"
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self):
        super().__init__(self.error_name, self.message, self.status_code)

class WealthsimpleDownException(AppError):
    error_name = "WealthsimpleDownException"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message):
        super().__init__(self.error_name, message.strip(), self.status_code)
# class WrapperError(Exception):
#     def __init__(self, error_name, error_status):
#         self.error_name = error_name
#         self.error_status= error_status
#         print("Wrapper Error name and status")
#         print(self.error_name())
#         print(self.error_status)
#         super().__init__(str(error_name()))

#     def __str__(self):
#         return f"WrapperError: {self.args[0]}"
    
# class LoginError(Exception):
#     """Error thrown when user login failed"""
    
#     def __init__(self):
#         self.error_status: status.HTTP_401_UNAUTHORIZED
#         super(LoginError, self).__init__("A Login Error has occurred")

# class MethodInputError(Exception):
#     """Error thrown when an input to a method is unacceptable"""

#     def __init__(self, message):
#         self.error_status: status.HTTP_422_UNPROCESSABLE_ENTITY
#         super(MethodInputError, self).__init__(str(message).strip())


# class EmptyTokensError(Exception):
#     """Error thrown when an tokens list is empty"""

#     def __init__(self):
#         self.error_status: status.HTTP_422_UNPROCESSABLE_ENTITY
#         super(EmptyTokensError, self).__init__("tokens are empty?")


# class InvalidAccessTokenError(Exception):
#     """Error thrown when an access token is invalid"""

#     def __init__(self):
#         self.error_status: status.HTTP_401_UNAUTHORIZED
#         super(InvalidAccessTokenError, self).__init__(
#             "An Invalid access token error was given, please try again"
#         )


# class InvalidRefreshTokenError(Exception):
    
#     """Error thrown when an refresh token is invalid"""

#     def __init__(self):
#         self.error_status: status.HTTP_401_UNAUTHORIZED
#         super(InvalidRefreshTokenError, self).__init__(
#             "An Invalid refresh token error was given, please try again"
#         )


# class OTPCallbackNone(Exception):
#     """Error thrown when otp_callback == None"""

#     def __init__(self):
#         self.error_status: status.HTTP_500_INTERNAL_SERVER_ERROR
#         super(OTPCallbackNone, self).__init__(
#             "An wealthsimple otp user account was triggered, please use a callback function"
#         )


# class WSOTPError(Exception):
#     """Error thrown when an otp error occurs"""

#     def __init__(self):
#         self.error_status: status.HTTP_400_BAD_REQUEST
#         super(WSOTPError, self).__init__(
#             "Otp is null, try again with your authenticating method"
#         )


# class WSOTPLoginError(Exception):
#     """Error thrown when an otp login error occurs"""

#     def __init__(self):
#         self.error_status: status.HTTP_400_BAD_REQUEST
#         super(WSOTPLoginError, self).__init__(
#             "A Wealthsimple otp login error happend, please try again"
#         )


# class TSXStopLimitPriceError(Exception):
#     """Error thrown when a stop order with a diffrent stop and limit price is made on a TSX/TSX-V securities"""

#     def __init__(self):
#         super(TSXStopLimitPriceError, self).__init__(
#             "TSX/TSX-V securities must have an equivalent stop and limit price"
#         )


# class WealthsimpleServerError(Exception):
#     """Error thrown when a endpoint returns a 5XX http code"""

#     def __init__(self, message):
#         self.error_status: status.HTTP_500_INTERNAL_SERVER_ERROR
#         super(WealthsimpleServerError, self).__init__(
#             "Wealthsimple endpoint might be down: return a 5XX http code"
#         )

# class RouteNotFoundException(Exception):
#     """Error thrown when a endpoint returns a 5XX http code"""

#     def __init__(self):
#         self.error_status: status.HTTP_404_NOT_FOUND
#         super(RouteNotFoundException, self).__init__(
#             "Wealthsimple endpoint not found: return a 404 http code"
#         )

# class WealthsimpleDownException(Exception):
#     """Error thrown when an input to a method is unacceptable"""
    
#     def __init__(self, message):
#         self.error_status: status.HTTP_500_INTERNAL_SERVER_ERROR
#         super(WealthsimpleDownException, self).__init__(str(message).strip())

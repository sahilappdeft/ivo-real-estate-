import math
import random


# Random OTP generation
def generateOTP():
    digits = "0123456789"
    otpLength = 8
    otp = ""

    i = 0
    while i < otpLength:
        index = math.floor(random.random() * len(digits))
        otp = otp + digits[index]
        i += 1

    return otp

# Success middleware
def success(message, data):
    res = {
        'success': True,
        'message': message,
        'data': data,
    }
    return res


# Error middleware
def error(message, data):
    res = {
        'success': False,
        'message': message,
        'data': data,
    }
    return res

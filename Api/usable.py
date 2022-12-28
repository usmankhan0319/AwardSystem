import re
from decouple import config
import jwt

def checkemailforamt(email):
    emailregix = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(re.match(emailregix, email)):

        return True

    else:
       return False




def passwordLengthValidator(passwd):
    if len(passwd) >= 8 and len(passwd) <= 20:
        return True

    else:
        return False


#Token Expire
def tokenauth(token):

    try:
       
        my_token = jwt.decode(token,config('adminkey'), algorithms=["HS256"])
        return my_token

    except jwt.ExpiredSignatureError:
        return False

    except:
        return False


def employeetokenauth(token):

    try:
       
        my_token = jwt.decode(token,config('employeekey'), algorithms=["HS256"])
        return my_token

    except jwt.ExpiredSignatureError:
        return False

    except:
        return False


import email.utils
import os
import re
import smtplib
import ssl
import string
from email.mime.text import MIMEText
from random import choice, randint, shuffle

import dns.resolver
import jwt
from werkzeug.security import check_password_hash, generate_password_hash

from data import users
from error import InputError

##########################################################################################
###                                  HELPER FUNCTIONS                                  ###
##########################################################################################
SECRET = "tue15mango1-FTW"


def is_valid_email(email):
    '''
    Normalizes email to all lowercase characters,
    then try resolving domain part of email to ensure that it is a valid email domain
    Check if email conforms to email regex specified in documentation.
    Parameter:
        email
    Returns:
        email (normalized)
    Exception:
        InputError: Email is unreachable or incorrect format
    '''
    email.lower()
    try:
        _, domain = email.split('@')
    except ValueError:
        raise InputError(description='Invalid email format')

    try:
        dns.resolver.resolve(domain, 'MX')
    except Exception as e:
        raise InputError(description=f'Cannot resolve {domain}:\n\t{e}') from e

    # emailregex.com
    regex = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    if not re.search(regex, email):
        raise InputError(description='Invalid email format')

    return email


def check_valid_name(name):
    '''
    Check if name is valid:
    Length: between 1 - 50
    Allow dash, space, and English alphabet. Reject everything else.
    '''
    if not 0 < len(name) <= 50:
        return False

    # remove '-' and ' '
    name = re.sub(r'[-\s]+', '', name)

    if re.search(r'[\W\d]', name):
        return False

    return True


def has_handle_conflict(handle):
    '''
    Detects handle conflicts by looping through list of user dictionaries
    '''
    if handle == "":
        return True

    global users
    for user in users:
        if user['handle'] == handle:
            return True

    return False


def generate_handle(name):
    '''
    Generate handle name, make everything lowercase
    Maxed at 20 characters, takes last 20 characters if exceeds max length (20)
    '''
    name = name.lower()
    return name[-20:] if len(name) > 20 else name


def generate_token(payload):
    '''
    Generate smart tokens using pyJWT, with `key=SECRET` as global variable
    Parameter:
        payload (dictionary with keys: ['u_id', 'email'])
    Returns:
        token (string)
    '''
    return jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')


##########################################################################################
###                                      AUTH_LOGIN                                    ###
##########################################################################################

def auth_login(email, password):
    '''
    Given a registered users' email and password,
    and generates a valid token for the user to remain authenticated
    Parameters:
        email, password
    Returns:
        dictionary: u_id, token
    '''
    global users

    email = is_valid_email(email)

    for user in users:
        if user['email'] == email:
            db_password = user['password']
            u_id = user['u_id']
            db_token = user['token']
            break
    else:
        raise InputError(description='Email invalid')

    if not check_password_hash(db_password, password):
        raise InputError(description='Incorrect password')

    payload = {
        'u_id': u_id,
        'email': email,
    }

    # if user is already logged in, pass token on record
    token = generate_token(payload) if db_token == "" else db_token

    for user in users:
        if user['u_id'] == u_id:
            user['token'] = token

    return {
        'u_id': u_id,
        'token': token
    }

##########################################################################################
###                                      AUTH_LOGOUT                                   ###
##########################################################################################


def auth_logout(token):
    '''
    Given an active token, invalidates the token to log user out.
    If a valid token is given, and the user is successfully logged
    out, it returns true, otherwise false.
    Parameters:
        token
    Returns:
        dictionary: is_success(boolean)
    '''
    global users
    for user in users:
        if user['token'] == token:
            user['token'] = ""
            is_success = True
            break
    else:
        is_success = False

    return {
        'is_success': is_success,
    }


##########################################################################################
###                                     AUTH_REGISTER                                  ###
##########################################################################################

def auth_register(email, password, name_first, name_last):
    '''
    Create a new account, with the given parameters.
    Return a token for authentication.
    Generate a handle
    Parameters:
        email, password, name_first, name_last
    Returns:
        dictionary : u_id, token
    '''
    global users

    email = is_valid_email(email)

    for user in users:
        if user['email'] == email:
            raise InputError(description='Email already used')

    if len(password) < 6:
        raise InputError(description='Password must be more than 6 characters')

    if not (check_valid_name(name_first) and check_valid_name(name_last)):
        raise InputError(description='Invalid first name or last name')

    # generate handle str
    handle_conflict = has_handle_conflict("")
    full_name = name_first + name_last
    while handle_conflict:
        handle = generate_handle(full_name)
        handle_conflict = has_handle_conflict(handle)
        if handle_conflict:
            full_name += str(randint(0, 999))

    # hash password
    password = generate_password_hash(password, 'sha256', salt_length=8)

    u_id = len(users)
    permission_id = 2
    if u_id == 0:
        permission_id = 1

    payload = {
        'u_id': u_id,
        'email': email,
    }

    token = generate_token(payload)
    new_user = {
        'u_id': u_id,
        'token': token,
        'password': password,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle': handle,
        'channels': [],
        'global_permission': permission_id,
        "profile_img_url" : "",
        'reset_code': ""
    }
    users.append(new_user)

    return {
        'u_id': u_id,
        'token': token,
    }


##########################################################################################
###                            AUTH_PASSWORDRESET_RESET                                ###
##########################################################################################
def auth_passwordreset_reset(reset_code, new_password):
    '''
    Given a reset code for a user,
    set that user's new password to the password provided
    Parameters:
        reset_code, new_password
    Returns:
        {}
    Exception, InputError:
        - reset_code invalid
        - new_password invalid
    '''
    reset_code = reset_code.upper()
    if len(reset_code) != 6:
        raise InputError(description=f'Reset code [{reset_code}] invalid')

    if len(new_password) < 6:
        raise InputError(description='Password must be more than 6 characters')

    new_password = generate_password_hash(new_password, 'sha256', salt_length=8)
    for user in users:
        if reset_code == user['reset_code']:
            user['password'] = new_password
            user['reset_code'] = ""
            break
    else:
        raise InputError(description=f'Reset code [{reset_code}] invalid')

    return {}


def generate_code():
    '''
    Generate reset codes, takes 3 letters and 3 digits,
    shuffle, and join back to string
    '''
    code = ""
    for _ in range(3):
        code += choice(string.ascii_uppercase)
        code += choice(string.digits)

    code = list(code)
    shuffle(code)
    return ''.join(code)


##########################################################################################
###                             AUTH_PASSWORDRESET_REQUEST                             ###
##########################################################################################
def auth_passwordreset_request(reset_email):
    '''
    Given an email address, if the user is a registered user,
    send them an email containing a specific secret code,
    Enter code in auth_passwordreset_reset
    If email is not registered or invalid, ignore
    https://pymotw.com/2/smtpd/
    https://realpython.com/python-send-email/
    Parameters: reset_email
    Returns: {}
    Exceptions: N/A
    '''
    if reset_email not in [user['email'] for user in users]:
        return {}

    while True:
        code = generate_code()
        if code not in [user['reset_code'] for user in users]: # pragma: no branch
            break

    if os.environ.get('TESTING') == "True":
        msg = MIMEText(f'CODE: {code}', 'utf-8')
        msg['To'] = email.utils.formataddr(('Recipient', reset_email))
        msg['From'] = email.utils.formataddr(('Author', 'admin@flockr-mailer.com'))
        msg['Subject'] = 'Password reset code'

        server = smtplib.SMTP('127.0.0.1', 1025)
        try:
            server.sendmail('admin@flockr-mailer.com', [reset_email], msg.as_string())
        finally:
            server.quit()
    else:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "tue15mango1.flockr@gmail.com"
        password = "tue15mango1-FTW"
        receiver_email = reset_email
        message = f"This is your reset code.\nCODE: {code}"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    for user in users:
        if user['email'] == reset_email:
            user['reset_code'] = code

    return {}

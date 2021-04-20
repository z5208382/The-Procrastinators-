import os
import time
import threading
import pytest
from auth import (
    auth_login,
    auth_logout,
    auth_register,
    auth_passwordreset_reset,
    auth_passwordreset_request,
)
from error import InputError
from other import clear
from mail_receiver import runner as mail_server


def register(a):
    '''
    Register a user for testing
    Assumes auth_register works
    '''
    user = auth_register(a + "email@email.com", "1234abcd", "First" + a, "Last" + a)

    u_id = user['u_id']
    token = user['token']
    return [u_id, token]


##########################################################################################
###                                 AUTH_REGISTER TESTS                                ###
##########################################################################################

def test_register_invalid_email():
    '''
    Test 1: Register user using invalid email (domain can't be resolved)
    '''
    clear()
    with pytest.raises(InputError):
        auth_register('bademail@abcd.qwerty', '123abc!@#', 'Bob', 'The builder')


def test_register_email_already_used():
    '''
    Test 2: Register with same email twice, expect InputError to be raised
    '''
    clear()
    auth_register('abcd@aa.com', '1234abcd', 'Gabe', 'Newell')
    with pytest.raises(InputError):
        auth_register('abcd@aa.com', '1234abcd', 'Gabe', 'Newell')


def test_password_invalid():
    '''
    Test 3: Register user with an invalid password (length too short)
    '''
    clear()
    with pytest.raises(InputError):
        auth_register('abcd@aa.com', '1234', 'Gabe', 'Newell')


def test_invalid_name():
    '''
    Test 4: Register with invalid name:
        - Numbers
        - Symbols
        - Too short
        - Too long
    '''
    clear()
    with pytest.raises(InputError):
        auth_register('abcd@aa.com', '1234abcd', 'G4b3', 'N3w3ll')

    clear()
    with pytest.raises(InputError):
        auth_register('abcd@aa.com', '1234abcd', 'G4b3', 'N3w3ll!')

    clear()
    with pytest.raises(InputError):
        auth_register('abcd@aa.com', '1234abcd', '', 'Empty')

    clear()
    with pytest.raises(InputError):
        auth_register('abcd@aa.com', '1234abcd', 'tekashi' * 69, 'Hehe')


def test_handle_conflict():
    '''
    Test 5: Force a handle conflict,
    the system should be able to resolve it automatically
    '''
    clear()
    auth_register('legit_email@gmail.com', '123456abcd', 'Gabe', 'Newell')
    auth_register('an_email@gmail.com', '123456abcd', 'Gabe', 'Newell')


##########################################################################################
###                                  AUTH_LOGIN TESTS                                  ###
##########################################################################################

def test_valid_login():
    '''
    Test 1: Test logging in
    Expect to work since we registered
    '''
    clear()
    auth_register('random@gmail.com', '123abc!@#', 'Bro', 'Howard')
    result = auth_register('validemail@gmail.com', '123abc!@#', 'Timothy', 'Howard')
    assert auth_login('validemail@gmail.com', '123abc!@#') == result


def test_invalid_email_login():
    '''
    Test 2: Test logging in
    Expect fail since e-mail has never been registered
    '''
    clear()
    result = auth_register('validemail@gmail.com', '123abc!@#', 'Timothy', 'Howard')
    with pytest.raises(InputError):
        auth_login('didntusethis@gmail.com', '123abcd!@#') == result


def test_invalid_password_login():
    '''
    Test 3: Test logging in
    Expect fail since password is wrong
    '''
    clear()
    result = auth_register('validemail@gmail.com', '123abc!@#', 'Tom', 'Cruise')
    with pytest.raises(InputError):
        auth_login('validemail@gmail.com', 'notsamep@55word') == result


def test_login_invalid_email():
    '''
    Test 4: Test logging in
    Expect fail since email is wrong
    '''
    clear()
    auth_register('bademail@icloud.com', '123abc!@#', 'Bob', 'The builder')
    with pytest.raises(InputError):
        auth_login('bademail@abcd.qwerty', '123abc!@#')


##########################################################################################
###                                  AUTH_LOGOUT TESTS                                 ###
##########################################################################################

def test_valid_logout():
    '''
    Test 1: A normal logout operation
    '''
    clear()
    token1 = register('a')[1]
    assert auth_logout(token1) == {'is_success': True}


def test_logout_invalid_token():
    '''
    Test 2: Log out with invalid token,
    expect 'is_success' to be false
    '''
    clear()
    auth_register('abcd@aa.com', '1234abcd', 'Gabe', 'Newell')
    is_success = auth_logout('not_a_valid_token')['is_success']
    assert not is_success


##########################################################################################
###                           AUTH_PASSWORDRESET_RESET TESTS                            ###
##########################################################################################

def test_passwordreset_reset_invalid_reset_code():
    '''
    Test 1: reset_code passed in is not valid
    Expecting InputError
    '''
    clear()
    _, token = register('a')
    auth_logout(token)

    threading.Thread(
        target=mail_server,
        args=(5,),
        daemon=True
    ).start()
    time.sleep(0.3)
    auth_passwordreset_request('aemail@email.com')


    with pytest.raises(InputError):
        auth_passwordreset_reset('invalid-code', 'password1234')


def test_paswordreset_reset_without_request():
    '''
    Test 2: reset password when not requested
    Expect InputError as reset_code is not generated, and emailed
    '''
    clear()
    _, token = register('a')
    auth_logout(token)

    with pytest.raises(InputError):
        auth_passwordreset_reset('', 'password1234')


def delay_passwordreset_request(email, wait):
    '''
    Add delay before requesting a password reset
    To allow mail server to start
    '''
    time.sleep(wait)
    auth_passwordreset_request(email)

def test_passwordreset_reset_invalid_new_password():
    '''
    Test 3: password passed in is not valid
    Expecting InputError
    '''
    clear()
    _, token = register('a')
    auth_logout(token)

    threading.Thread(
        target=delay_passwordreset_request,
        args=('aemail@email.com', 0.5),
        daemon=True
    ).start()

    code = mail_server(5)
    time.sleep(0.3)
    with pytest.raises(InputError):
        auth_passwordreset_reset(code, 'nope')


def test_passwordreset_reset_wrong_code():
    '''
    Test 4: Six characters entered, but not in database
    '''
    clear()
    _, token = register('a')
    auth_logout(token)

    threading.Thread(
        target=delay_passwordreset_request,
        args=('aemail@email.com', 0.5),
        daemon=True
    ).start()
    mail_server(5)

    with pytest.raises(InputError):
        auth_passwordreset_reset('AAAAAA', 'iliekbread')


def test_passwordreset_reset_valid():
    '''
    Test 5: Valid password reset.
    User should be able to use new password to login
    '''
    clear()
    u_id, token = register('a')
    auth_logout(token)

    email = 'aemail@email.com'
    threading.Thread(
        target=delay_passwordreset_request,
        args=(email, 0.5),
        daemon=True
    ).start()

    code = mail_server(5)
    time.sleep(0.3)

    new_password = 'password1234'
    auth_passwordreset_reset(code, new_password)

    # should work when logging in with new password
    assert u_id == auth_login(email, new_password)['u_id']

def test_passwordreset_reset_valid_multi():
    '''
    Test 6: Valid password reset. Multiple users.
    With 4 users, all of them requests a password reset.
    Then they reset to a new password, and verify that they can
    login and logout with new credentials
    '''
    clear()
    for i in 'abcd':
        _, token = register(i)
        auth_logout(token)

    email = 'email@email.com'

    codes = []
    for i in 'bcda':
        threading.Thread(
            target=delay_passwordreset_request,
            args=(f'{i}{email}', 0.2),
            daemon=True
        ).start()
        code = mail_server(1)
        time.sleep(0.3)
        codes.append(code)

    for t, i in enumerate('bcda'):
        new_password = 'password1234'
        auth_passwordreset_reset(codes[t], new_password)
        token = auth_login(f'{i}{email}', new_password)['token']
        assert auth_logout(token)['is_success']


################################################################################
###                    AUTH_PASSWORDRESET_REQUEST TESTS                      ###
################################################################################

def test_request_invalid_email():
    '''
    Test 1: If the input email does not exist in the users database,
    assume they are not a registered user
    Do nothing
    '''
    clear()
    auth_passwordreset_request('doesnotexist@hotmail.com')


def test_request_valid():
    '''
    Test 2: Valid request,
    user is registered and requests a password reset with same email
    '''
    clear()
    _, token = register('a')
    auth_logout(token)

    email = 'aemail@email.com'
    threading.Thread(
        target=delay_passwordreset_request,
        args=(email, 0.5),
        daemon=True
    ).start()

    code = mail_server(5)
    time.sleep(0.3)

    assert len(code) == 6


def test_request_non_testing():
    '''
    Test 3: Send email to an actual email address
    Change TESTING environment variable to empty string,
    Can't test if code is sent correctly with pytest
    '''
    os.environ['TESTING'] = ""
    clear()
    _, token = register('a')
    auth_logout(token)
    email = 'aemail@email.com'
    auth_passwordreset_request(email)
    os.environ['TESTING'] = "True"

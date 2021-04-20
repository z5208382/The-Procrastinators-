import os
import json
import time
import threading
import requests

from other import clear
from auth import *
from channel import *
from user import *
from helper_server_tests import http_register
from mail_receiver import runner as mail_server

##########################################################################################
###                             ✨ AUTH/REGISTER HTTP TESTS ✨                        ###
##########################################################################################

def test_register_input_error_invalid_email(url):
    '''
    Test 1: email entered is not a valid email
    InputError is raised
    '''
    clear()
    resp = requests.post(url + '/auth/register', \
        json={
            'email': 'invalidemail.com',
            'password': 'validpassword123',
            'name_first': 'validfirst',
            'name_last': 'validlast'
        })
    assert resp.status_code == 400


def test_register_input_error_used_email(url):
    '''
    Test 2: email address is already being used by another user
    InputError is raised
    '''
    clear()
    http_register(url, 'Bob')
    resp = requests.post(url + '/auth/register', \
        json={
            'email': 'bob@gmail.com',
            'password': 'validpassword123',
            'name_first': 'validfirst',
            'name_last': 'validlast'
        })
    assert resp.status_code == 400


def test_register_input_error_invalid_password(url):
    '''
    Test 3: password entered is less than 6 characters long
    InputError is raised
    '''
    clear()
    resp = requests.post(url + '/auth/register', \
        json={
            'email': 'validemaill@gmail.com',
            'password': 'bad',
            'name_first': 'validfirst',
            'name_last': 'validlast'
        })
    assert resp.status_code == 400


def test_register_input_error_name_first(url):
    '''
    Test 4: name_first is not between 1 and 50 characters in length
    InputError is raised
    '''
    clear()
    resp = requests.post(url + '/auth/register', \
        json={
            'email': 'validemail@gmail.com',
            'password': 'validpassword123',
            'name_first': 'first' * 11,
            'name_last': 'validlast'
        })
    assert resp.status_code == 400


def test_register_input_error_name_last(url):
    '''
    Test 5: name_last is not between 1 and 50 characters in length
    InputError is raised
    '''
    clear()
    resp = requests.post(url + '/auth/register', \
        json={
            'email': 'validemail@gmail.com',
            'password': 'validpassword123',
            'name_first': 'validfirst',
            'name_last': 'last' * 13
        })
    assert resp.status_code == 400


def test_register_valid(url):
    '''
    Test 6: given a user's first and last name, email address and password,
    a new account is created for them
    return their u_id and token
    '''
    clear()
    resp = requests.post(url + '/auth/register', \
        json={
            'email': 'validemail@gmail.com',
            'password': 'validpassword123',
            'name_first': 'validfirst',
            'name_last': 'validlast'
        })
    assert resp.status_code == 200
    assert 'u_id' in json.loads(resp.text)
    assert 'token' in json.loads(resp.text)

##########################################################################################
###                                  ✨ AUTH/LOGIN TESTS ✨                             ###
##########################################################################################

def test_server_valid_login(url):
    '''
    Test 1: test user login is valid
    will return token and uid
    '''
    clear()
    user_info = {'email': 'validemail@gmail.com', 'password': '123abc!@#', \
        'name_first': 'Timothy', 'name_last': 'Howard'}
    register = requests.post(url + '/auth/register', json=user_info)
    auth_dict = json.loads(register.text)

    response = requests.post(url + '/auth/login', json={'email': \
        'validemail@gmail.com', 'password': '123abc!@#'})
    assert json.loads(response.text) == auth_dict


def test_server_invalid_email_login(url):
    '''
    Test 2: test user login is invalid - due to invalid email
    will return code for InputError
    '''
    clear()
    user_info = {'email': 'validemail@gmail.com', 'password': '123abc!@#', \
        'name_first': 'Timothy', 'name_last': 'Howard'}
    requests.post(url + '/auth/register', json=user_info)

    response = requests.post(url + '/auth/login', json={'email': \
        'didntusethis@gmail.com', 'password': '123abc!@#'})
    assert response.status_code == 400


def test_server_invalid_password_login(url):
    '''
    Test 3: test user login is invalid - due to invalid password
    will return code for InputError
    '''
    clear()
    user_info = {'email': 'validemail@gmail.com', 'password': '123abc!@#', \
        'name_first': 'Timothy', 'name_last': 'Howard'}
    requests.post(url + '/auth/register', json=user_info)

    response = requests.post(url + '/auth/login', json={'email': \
        'validemail@gmail.com', 'password': 'notsamep@55word'})
    assert response.status_code == 400


def test_server_login_invalid_email(url):
    '''
    Test 4: test user login is invalid - due to invalid email
    will return code for InputError
    '''
    clear()
    user_info = {'email': 'bademail@icloud.com', 'password': '123abc!@#', \
        'name_first': 'Timothy', 'name_last': 'Howard'}
    requests.post(url + '/auth/register', json=user_info)

    response = requests.post(url + '/auth/login', \
        json={'email': 'bademail@abcd.qwerty', 'password': '123abc!@#'})
    assert response.status_code == 400


##########################################################################################
###                                  ✨ AUTH/LOGOUT TESTS ✨                            ###
##########################################################################################

def test_server_valid_logout(url):
    '''
    Test 1: test user logout is valid
    will return success = True
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']

    response = requests.post(url + '/auth/logout', json={'token': token1})
    assert json.loads(response.text) == {'is_success': True}


def test_server_logout_invalid_token(url):
    '''
    Test 2: test user logout is invalid
    will return success = False
    '''
    clear()
    user_info = {'email': 'abcd@aa.com', 'password': '1234abcd', \
        'name_first': 'Gabe', 'name_last': 'Newell'}
    requests.post(url + '/auth/register', json=user_info)

    response = requests.post(url + '/auth/logout', json={'token': 'not_a_valid_token'})
    assert json.loads(response.text) == {'is_success': False}

##########################################################################################
###                           AUTH_PASSWORDRESET_RESET TESTS                            ###
##########################################################################################

def test_passwordreset_reset_invalid_reset_code(url):
    '''
    Test 1: reset_code passed in is not valid
    Expecting InputError
    '''
    clear()
    token = http_register(url, 'bob')['token']
    requests.post(f"{url}/auth/logout",
        json={'token' : token}
        )
    threading.Thread(
        target=mail_server,
        args=(5,),
        daemon=True
    ).start()
    time.sleep(0.3)
    requests.post(f"{url}/auth/passwordreset/request",
        json={'email' : 'aemail@email.com'}
        )
    resp = requests.post(f"{url}/auth/passwordreset/reset",
        json={'reset_code' : 'invalid-code',
            'new_password' : 'password1234'}
        )
    assert not resp.ok

def test_paswordreset_reset_without_request(url):
    '''
    Test 2: reset password when not requested
    Expect InputError as reset_code is not generated, and emailed
    '''
    clear()
    token = http_register(url, 'bob')['token']
    requests.post(f"{url}/auth/logout",
        json={'token' : token}
        )
    resp = requests.post(f"{url}/auth/passwordreset/reset",
        json={'reset_code' : '', 'new_password' : 'password1234'}
        )
    assert not resp.ok

def delay_server_passwordreset_request(url, email, wait):
    '''
    Add delay before requesting a password reset
    To allow mail server to start
    '''
    time.sleep(wait)
    requests.post(f"{url}/auth/passwordreset/request",
        json={'email' : email}
        )
    # auth_passwordreset_request(email)

def test_passwordreset_reset_invalid_new_password(url):
    '''
    Test 3: password passed in is not valid
    Expecting InputError
    '''
    clear()
    token = http_register(url, 'bob')['token']
    requests.post(f"{url}/auth/logout",
        json={'token' : token}
        )
    threading.Thread(
        target=delay_server_passwordreset_request,
        args=(url, 'bob@gmail.com', 0.5),
        daemon=True
    ).start()

    code = mail_server(5)
    time.sleep(0.3)
    resp = requests.post(f"{url}/auth/passwordreset/reset",
        json={'reset_code' : code, 'new_password' : 'nope'}
        )
    assert resp.status_code == 400

def test_passwordreset_reset_wrong_code(url):
    '''
    Test 4: Six characters entered, but not in database
    '''
    clear()
    token = http_register(url, 'bob')['token']
    requests.post(f"{url}/auth/logout",
        json={'token' : token}
        )
    threading.Thread(
        target=delay_server_passwordreset_request,
        args=(url, 'bob@gmail.com', 0.5),
        daemon=True
    ).start()
    mail_server(5)
    resp = requests.post(f"{url}/auth/passwordreset/reset",
        json={'reset_code' : 'AAAAAA', 'new_password' : 'iliekbread'}
        )
    assert resp.status_code == 400


def test_passwordreset_reset_valid(url):
    '''
    Test 5: Valid password reset.
    User should be able to use new password to login
    '''
    clear()
    u_id, token = http_register(url, 'bob').values()
    requests.post(f"{url}/auth/logout",
        json={'token' : token}
        )
    email = 'bob@gmail.com'
    threading.Thread(
        target=delay_server_passwordreset_request,
        args=(url, email, 0.5),
        daemon=True
    ).start()

    code = mail_server(5)
    time.sleep(0.3)

    new_password = 'password1234'
    requests.post(f"{url}/auth/passwordreset/reset",
        json={'reset_code' : code, 'new_password' : new_password}
        )

    resp = requests.post(f"{url}/auth/login",
        json={'email' : email, 'password' : new_password}
        )
    assert resp.json()['u_id'] == u_id

def test_passwordreset_reset_valid_multi(url):
    '''
    Test 6: Valid password reset. Multiple users.
    With 4 users, all of them requests a password reset.
    Then they reset to a new password, and verify that they can
    login and logout with new credentials
    '''
    clear()
    name_list = ['bob', 'sarah', 'lucy', 'jessica']
    for i in name_list:
        token = http_register(url, i)['token']
        requests.post(f"{url}/auth/logout",
        json={'token' : token}
        )
    email = '@gmail.com'

    name_list.reverse()
    new_list = name_list
    codes = []
    for i in new_list:
        threading.Thread(
            target=delay_server_passwordreset_request,
            args=(url, f'{i}{email}', 0.2),
            daemon=True
        ).start()
        code = mail_server(1)
        time.sleep(0.3)
        codes.append(code)

    for t, i in enumerate(new_list):
        new_password = 'password1234'
        requests.post(f"{url}/auth/passwordreset/reset",
            json={'reset_code' : codes[t], 'new_password' : new_password}
            )
        token = requests.post(f"{url}/auth/login",
            json={'email' : f'{i}{email}', 'password' : new_password}
            ).json()['token']
        assert requests.post(f'{url}/auth/logout',
            json={'token' : token}).json()['is_success']

################################################################################
###                    AUTH_PASSWORDRESET_REQUEST TESTS                      ###
################################################################################

def test_request_invalid_email(url):
    '''
    Test 1: If the input email does not exist in the users database,
    assume they are not a registered user
    Do nothing
    '''
    clear()
    email = 'doesnotexist@hotmail.com'
    requests.post(f"{url}/auth/passwordreset/request", json={'email' : email})

def test_request_valid(url):
    '''
    Test 2: Valid request,
    user is registered and requests a password reset with same email
    '''
    clear()
    token = http_register(url, 'bob')['token']
    requests.post(f"{url}/auth/logout", json={'token' : token})

    email = 'bob@gmail.com'
    threading.Thread(
        target=delay_server_passwordreset_request,
        args=(url, email, 0.5),
        daemon=True
    ).start()

    code = mail_server(5)
    time.sleep(0.3)

    assert len(code) == 6

def test_request_non_testing(url):
    '''
    Test 3: Send email to an actual email address
    Change TESTING environment variable to empty string,
    Can't test if code is sent correctly with pytest
    '''
    os.environ['TESTING'] = ""
    clear()
    token = http_register(url, 'bob')['token']
    requests.post(f"{url}/auth/logout", json={'token' : token})
    email = 'bob@gmail.com'
    requests.post(f"{url}/auth/passwordreset/request",
        json={'email' : email}
        )
    os.environ['TESTING'] = 'True'

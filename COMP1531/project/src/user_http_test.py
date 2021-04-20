import json
import requests
from server import *
from other import clear
from helper_server_tests import http_register
from echo_http_test import *


##########################################################################################
###                                 USER/PROFILE TESTS                                 ###
##########################################################################################
def test_profile_invalid_token(url):
    '''
    Test 1: invalid token is given
    AccessError is raised
    '''
    clear()
    u_id, token = http_register(url, 'Bob').values()
    resp = requests.get(url + '/user/profile', \
        params={
            'token': token + 'a',
            'u_id': u_id
        })
    assert resp.status_code == 400


def test_profile_input_error(url):
    '''
    Test 2: user with u_id is not a valid user
    InputError is raised
    '''
    clear()
    u_id, token = http_register(url, 'Bob').values()
    resp = requests.get(url + '/user/profile', \
        params={
            'token': token,
            'u_id': u_id + 2
        })
    assert resp.status_code == 400


def test_profile_self(url):
    '''
    Test 3: authorised user requests their own profile
    '''
    clear()
    u_id, token = http_register(url, 'Bob').values()
    resp = requests.get(url + '/user/profile', \
        params={
            'token': token,
            'u_id': u_id
        })
    assert resp.status_code == 200
    assert json.loads(resp.text)['user'] == {
        'u_id': u_id,
        'email': 'bob@gmail.com',
        'name_first': 'Bob',
        'name_last': 'Bob',
        'handle_str': 'bobbob',
        'profile_img_url': ''
    }

def test_profile_other(url):
    '''
    Test 4: authorised user requests another user's profile
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    u_id2 = http_register(url, 'Sally')['u_id']
    resp = requests.get(url + '/user/profile', \
        params={
            'token': token1,
            'u_id': u_id2
        })
    assert resp.status_code == 200
    assert json.loads(resp.text)['user'] == {
        'u_id': u_id2,
        'email': 'sally@gmail.com',
        'name_first': 'Sally',
        'name_last': 'Sally',
        'handle_str': 'sallysally',
        'profile_img_url': '',
    }


##########################################################################################
###                             USER/PROFILE/SETNAME TESTS                             ###
##########################################################################################
def test_profile_setname_invalid_token(url):
    '''
    Test 1: invalid token is given
    AccessError is raised
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.put(url + '/user/profile/setname', \
        json={
            'token': token + 'a',
            'name_first': 'newfirst',
            'name_last': 'newlast'
        })
    assert resp.status_code == 400


def test_setname_input_error_first(url):
    '''
    Test 2: name_first is not between 1 and 50 characters in length
    InputError raised
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.put(url + '/user/profile/setname', \
        json={
            'token': token,
            'name_first': '',
            'name_last': 'NewLast'
        })
    assert resp.status_code == 400


def test_setname_input_error_last(url):
    '''
    Test 3: name_last is not between 1 and 50 characters in length
    InputError is raised
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.put(url + '/user/profile/setname', \
        json={
            'token': token,
            'name_first': 'NewFirst',
            'name_last': 'NewLast' * 8
        })
    assert resp.status_code == 400


def test_setname_valid(url):
    '''
    Test 4: update authorised user's name
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.put(url + '/user/profile/setname', \
        json={
            'token': token,
            'name_first': 'NewFirst',
            'name_last': 'NewLast'
        })
    assert resp.status_code == 200



##########################################################################################
###                            USER/PROFILE/SETEMAIL TESTS                             ###
##########################################################################################
def test_profile_setemail_invalid_token(url):
    '''
    Test 1: invalid token is given
    AccessError is raised
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.put(url + '/user/profile/setemail', \
        json={
            'token': token + 'a',
            'email': 'validemail@gmail.com'
        })
    assert resp.status_code == 400


def test_setemail_input_error_invalid(url):
    '''
    Test 2: email entered is not a valid email
    InputError is raised
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.put(url + '/user/profile/setemail', \
        json={
            'token': token,
            'email': 'invalidemail.com'
        })
    assert resp.status_code == 400


def test_setemail_input_error_used(url):
    '''
    Test 3: email address is already being used by another user
    InputError is raised
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    http_register(url, 'Sally')
    resp = requests.put(url + '/user/profile/setemail', \
        json={
            'token': token1,
            'email': 'sally@gmail.com'
        })
    assert resp.status_code == 400


def test_setemail_valid(url):
    '''
    Test 4: update authorised user's email address
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.put(url + '/user/profile/setemail', \
        json={
            'token': token,
            'email': 'newemail@gmail.com'
        })
    assert resp.status_code == 200



##########################################################################################
###                            USER/PROFILE/SETHANDLE TESTS                            ###
##########################################################################################
def test_profile_sethandle_invalid_token(url):
    '''
    Test 1: invalid token is given
    AccessError is raised
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.put(url + '/user/profile/sethandle', \
        json={
            'token': token + 'a',
            'handle_str': 'newhandle'
        })
    assert resp.status_code == 400


def test_sethandle_input_error_length(url):
    '''
    Test 2: handle_str is not between 3 and 20 characters in length
    InputError is raised
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.put(url + '/user/profile/sethandle', \
        json={
            'token': token,
            'handle_str': 'a'
        })
    assert resp.status_code == 400


def test_sethandle_input_error_used(url):
    '''
    Test 3: handle_str is already being used by another user
    InputError is raised
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    http_register(url, 'Sally')
    resp = requests.put(url + '/user/profile/sethandle', \
        json={
            'token': token,
            'handle_str': 'sallysally'
        })
    assert resp.status_code == 400


def test_sethandle_valid(url):
    '''
    Test 4: update authorised user's handle
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.put(url + '/user/profile/sethandle', \
        json={
            'token': token,
            'handle_str': 'newhandle'
        })
    assert resp.status_code == 200

##########################################################################################
###                            USER/PROFILE/UPLOADPHOTO TESTS                          ###
##########################################################################################

def test_http_uploadphoto_invalid_token(url):
    '''
    Test 1: If invalid token is input
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    resp = requests.post(url + 'user/profile/uploadphoto', json={'token': token + 'a',\
    'img_url': img_url, 'x_start': 0, 'y_start': 0, 'x_end': 75, 'y_end': 40})

    assert resp.status_code == 400

def test_http_uploadphoto_invalid_url(url):
    '''
    Test 2: If img_url is invalid/does not raise http code of 200
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    img_url = "https://i.imgur.com/QLMuFYp.jpe"
    resp = requests.post(url + 'user/profile/uploadphoto', json={'token': token,\
    'img_url': img_url, 'x_start': 0, 'y_start': 0, 'x_end': 75, 'y_end': 40})

    assert resp.status_code == 400

def test_http_xstart_invalid(url):
    '''
    Test 3: If x_start is invalid/out of bounds
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    resp = requests.post(url + 'user/profile/uploadphoto', json={'token': token,\
    'img_url': img_url, 'x_start': -1, 'y_start': 0, 'x_end': 75, 'y_end': 40})

    assert resp.status_code == 400

def test_http_ystart_invalid(url):
    '''
    Test 4: If y_start is invalid/out of bounds
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    resp = requests.post(url + 'user/profile/uploadphoto', json={'token': token,\
    'img_url': img_url, 'x_start': 0, 'y_start': -1, 'x_end': 75, 'y_end': 40})

    assert resp.status_code == 400

def test_http_xend_invalid(url):
    '''
    Test 5: If y_end is invalid/out of bounds
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    resp = requests.post(url + 'user/profile/uploadphoto', json={'token': token,\
    'img_url': img_url, 'x_start': 0, 'y_start': 0, 'x_end': 71000, 'y_end': 40})

    assert resp.status_code == 400

def test_http_yend_invalid(url):
    '''
    Test 6: If y_end is invalid/out of bounds
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    resp = requests.post(url + 'user/profile/uploadphoto', json={'token': token,\
    'img_url': img_url, 'x_start': 0, 'y_start': 0, 'x_end': 75, 'y_end': 40000})

    assert resp.status_code == 400

def test_http_not_jpg(url):
    '''
    Test 7: If img_url is not a jpg
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    img_url =\
        "https://freepngimg.com/thumb/the_legend_of_zelda/21540-1-zelda-link-transparent.png"
    resp = requests.post(url + 'user/profile/uploadphoto', json={'token': token,\
    'img_url': img_url, 'x_start': 0, 'y_start': 0, 'x_end': 75, 'y_end': 40})

    assert resp.status_code == 400

def test_http_uploadphoto_valid(url):
    '''
    Test 8: User successfully uploads a photo
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    resp = requests.post(url + 'user/profile/uploadphoto', json={'token': token,\
    'img_url': img_url, 'x_start': 0, 'y_start': 0, 'x_end': 250, 'y_end': 240})

    assert resp.status_code == 200
    assert json.loads(resp.text) == {}

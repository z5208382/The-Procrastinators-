import json
import requests
from helper_tests import *
from server import *
from other import clear
from helper_server_tests import *

##########################################################################################
###                                  CHANNELS/LIST TESTS                               ###
##########################################################################################
def test_list_invalid_token(url):
    '''
    Test 1: If an invalid token is input
    Raise AccessError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.get(url + 'channels/list', params={'token': token + 'a'})
    assert resp.status_code == 400

def test_lists_empty(url):
    '''
    Test 2: If the user is not in any channels_create
    Return empty channels list
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.get(url + 'channels/list', params={'token': token})
    assert resp.status_code == 200
    assert json.loads(resp.text) == {'channels': []}

def test_lists_basic(url):
    '''
    Test 3: If the user is in one channel
    Return that channel when channels_list is called
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_one = http_create_public_channel(url, token, 'Channel1')
    channel_d = requests.get(url + 'channel/details',\
                             params={'token': token, 'channel_id': channel_one})
    resp = requests.get(url + 'channels/list', params={'token': token})
    channel_one_details = channel_d.json()
    assert resp.status_code == 200
    assert json.loads(resp.text) == {
        "channels": [
            {"name": channel_one_details['name'], "channel_id": channel_one}
            ]
    }

def test_lists_public_private(url):
    '''
    Test 4: Make sure both private and public channels that the
    user is in are returned
    '''
    clear()
    token = http_register(url, 'Bob')['token']

    channel_publ = http_create_public_channel(url, token, 'Channel1')
    channel_priv = http_create_private_channel(url, token, 'Channel2')

    channel_publ_d = requests.get(url + 'channel/details',\
                            params={'token': token, 'channel_id': channel_publ})
    channel_priv_d = requests.get(url + 'channel/details',\
                            params={'token': token, 'channel_id': channel_priv})
    resp = requests.get(url + 'channels/list', params={'token': token})

    channel_priv_details = channel_priv_d.json()
    channel_publ_details = channel_publ_d.json()
    assert resp.status_code == 200
    assert json.loads(resp.text) == {
        "channels": [
            {"name": channel_publ_details['name'], "channel_id": channel_publ},
            {"name": channel_priv_details['name'], "channel_id": channel_priv}
            ]
    }

##########################################################################################
###                            CHANNELS/LISTALL TESTS                                  ###
##########################################################################################
def test_list_all_invalid_token(url):
    '''
    Test 1: If an invalid token is input
    Raise AccessError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.get(url + 'channels/listall',\
                                                  params={'token': token + 'a'})
    assert resp.status_code == 400

def test_list_all_empty(url):
    '''
    Test 2: If no channels exist
    Return empty channels list
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.get(url + 'channels/listall', params={'token': token})
    assert resp.status_code == 200
    assert json.loads(resp.text) == {'channels': []}

def test_list_all_basic(url):
    '''
    Test 3: Register 2 users
    One user is part of three public channels while the other is not part of any
    Make sure that all three channels are returned when either user tries to
    look at all channels
    '''
    clear()
    token1 = http_register(url, 'Bobx')['token']
    token2 = http_register(url, 'Boby')['token']

    channel_one = http_create_public_channel(url, token1, 'Channel1')
    channel_two = http_create_public_channel(url, token1, 'Channel2')
    channel_three = http_create_public_channel(url, token1, 'Channel3')

    channel_one_d = requests.get(url + 'channel/details',\
                            params={'token': token1, 'channel_id': channel_one})
    channel_two_d = requests.get(url + 'channel/details',\
                            params={'token': token1, 'channel_id': channel_two})
    channel_three_d = requests.get(url + 'channel/details',\
                          params={'token': token1, 'channel_id': channel_three})

    channel_one_details = channel_one_d.json()
    channel_two_details = channel_two_d.json()
    channel_three_details = channel_three_d.json()

    resp1 = requests.get(url + 'channels/listall', params={'token': token1})
    assert resp1.status_code == 200
    assert json.loads(resp1.text) == {
        "channels": [
            {"name": channel_one_details['name'], "channel_id": channel_one},
            {"name": channel_two_details['name'], "channel_id": channel_two},
            {"name": channel_three_details['name'], "channel_id": channel_three}
            ]
    }

    resp2 = requests.get(url + 'channels/listall', params={'token': token2})
    assert resp2.status_code == 200
    assert json.loads(resp2.text) == {
        "channels": [
            {"name": channel_one_details['name'], "channel_id": channel_one},
            {"name": channel_two_details['name'], "channel_id": channel_two},
            {"name": channel_three_details['name'], "channel_id": channel_three}
            ]
    }

def test_list_all_public_private(url):
    '''
    Test 4: Register 2 users
    One user is a part of one public channel and one private channel while the
    other user is only part of the public channel
    Make sure both public and private channels are returned when either user
    tries to look at all channels
    '''
    clear()
    token1 = http_register(url, 'Bobx')['token']
    token2 = http_register(url, 'Boby')['token']

    channel_publ = http_create_public_channel(url, token1, 'Channel1')
    channel_priv = http_create_private_channel(url, token1, 'Channel2')
    channel_publ_d = requests.get(url + 'channel/details',\
                           params={'token': token1, 'channel_id': channel_publ})
    channel_priv_d = requests.get(url + 'channel/details',\
                           params={'token': token1, 'channel_id': channel_priv})

    channel_priv_details = channel_priv_d.json()
    channel_publ_details = channel_publ_d.json()

    resp1 = requests.get(url + 'channels/listall', params={'token': token1})

    assert resp1.status_code == 200
    assert json.loads(resp1.text) == {
        "channels": [
            {"name": channel_publ_details['name'], "channel_id": channel_publ},
            {"name": channel_priv_details['name'], "channel_id": channel_priv}
            ]
    }

    requests.post(url + '/channel/join', json={'token': token2,
                                               'channel_id': channel_publ})

    resp2 = requests.get(url + 'channels/listall', params={'token': token2})
    assert resp2.status_code == 200
    assert json.loads(resp2.text) == {
        "channels": [
            {"name": channel_publ_details['name'], "channel_id": channel_publ},
            {"name": channel_priv_details['name'], "channel_id": channel_priv}
            ]
    }

##########################################################################################
###                                CHANNELS/CREATE TESTS                               ###
##########################################################################################
def test_create_invalid_token(url):
    '''
    Test 1: If an invalid token is input
    Raise AccessError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_name = "Invalidnameinputerror"
    resp = requests.post(url + '/channels/create', json={'token': token + 'a',
                                                         'name': channel_name,
                                                         'is_public': True
                                                         })
    assert resp.status_code == 400

def test_create_invalid_public(url):
    '''
    Test 2: When public channel name is over 20 characters long
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_name = "Invalidnameinputerror"

    resp = requests.post(url + '/channels/create', json={'token': token,
                                                         'name': channel_name,
                                                         'is_public': True
                                                         })
    assert resp.status_code == 400

def test_create_invalid_private(url):
    '''
    Test 3: When public channel name is over 20 characters long
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_name = "Invalidnameinputerror"

    resp = requests.post(url + '/channels/create', json={'token': token,
                                                         'name': channel_name,
                                                         'is_public': False
                                                         })
    assert resp.status_code == 400

def test_create_valid_public(url):
    '''
    Test 4: Make sure public channels can be successfully created
    Check channel_id is returned properly
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_name = "validname"

    resp = requests.post(url + '/channels/create', json={'token': token,
                                                         'name': channel_name,
                                                         'is_public': True
                                                         })
    channel_valid = resp.json()
    assert resp.status_code == 200
    assert json.loads(resp.text) == channel_valid

def test_create_valid_private(url):
    '''
    Test 5: Make sure private channels can be successfully created
    Check channel_id is returned properly
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_name = "validname"

    resp = requests.post(url + '/channels/create', json={'token': token,
                                                         'name': channel_name,
                                                         'is_public': False
                                                         })
    channel_valid = resp.json()
    assert resp.status_code == 200
    assert json.loads(resp.text) == channel_valid

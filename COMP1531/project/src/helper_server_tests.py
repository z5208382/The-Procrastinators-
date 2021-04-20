import json

import requests

from auth import *
from channel import *
from user import *

############################################################################################
###                 ✨ ✨ ✨ AUTH/REGISTER HELPER SERVER FUNCTIONS ✨ ✨ ✨           ###
############################################################################################

def http_register(url, name):
    '''
    Helper function to register user using `auth/register` route
    '''
    route = url + '/auth/register'
    payload = {
        'email': f'{name.lower()}@gmail.com',
        'password': '4r3allyG00dp4ssw0rd',
        'name_first': name,
        'name_last': name,
    }
    response = requests.post(route, json=payload)
    assert response.ok
    data = response.json()
    return {'u_id': data['u_id'], 'token': data['token']}

############################################################################################
###            ✨ ✨ ✨ CREATE/CHANNEL HELPER SERVER FUNCTIONS ✨ ✨ ✨               ###
############################################################################################

def http_create_public_channel(url, token, name):
    '''
    creates a public channel and returns its channel_id
    '''

    payload = {
        'token': token,
        'name': name,
        'is_public': True
    }
    create_channel = requests.post(url + '/channels/create', json=payload)

    channel_id = json.loads(create_channel.text)['channel_id']
    return channel_id


def http_create_private_channel(url, token, name):
    '''
    creates a private channel and returns its channel_id
    '''
    payload = {
        'token': token,
        'name': name,
        'is_public': False
    }
    create_channel = requests.post(url + '/channels/create', json=payload)
    channel_id = json.loads(create_channel.text)['channel_id']
    return channel_id


def http_load_message(url, name):
    '''
    Load messages in public and private channel
    Returns:
        {{user}, public, private}
    '''
    u_id, token = http_register(url, name).values()
    pub_channel = http_create_public_channel(url, token, 'pub')
    priv_channel = http_create_private_channel(url, token, 'priv')
    user = {'u_id': u_id, 'token': token}

    payload = {
        'token': token,
        'channel_id': '',
        'message':''
    }

    for i in "abcdaefghij":
        payload['message'] = i

        payload['channel_id'] = pub_channel
        requests.post(url + 'message/send', json=payload)

        payload['channel_id'] = priv_channel
        requests.post(url + 'message/send', json=payload)

    return {
        'user':user,
        'public': pub_channel,
        'private': priv_channel
    }

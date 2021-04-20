import jwt
from data import *
from error import AccessError, InputError
from auth import SECRET
global users
global channels

############################################################################################
###                          HELPER FUNCTIONS FOR IMPLEMENTATION                         ###
############################################################################################
def get_user_id(token):
    '''
    takes in a token and checks if it is valid
    if invalid, raises AccessError
    returns the corresponding user's u_id
    '''
    try:
        u_id = jwt.decode(token.encode('utf-8'), SECRET, algorithms=['HS256'])['u_id']
    except jwt.exceptions.InvalidTokenError as e:
        raise AccessError(description=f'Invalid token: {e}')

    for user in users:
        if user['u_id'] == u_id and user['token'] == token:
            return u_id
    else:
        raise AccessError(description='Invalid token, user not logged in')


def get_user_index(u_id):
    '''
    takes a u_id and returns the user's index in users database
    if u_id not found, raise InputError
    '''
    for i, user in enumerate(users):
        if u_id == user['u_id']:
            return i
    else:
        raise InputError(description=f'User with u_id {u_id} does not exist')


def check_user_in_channel(u_id, channel_id):
    '''
    takes a u_id and channel id and checks if the user is a member of the channel
    if invalid, raise AccessError
    '''
    for user in users:
        if u_id == user['u_id']:
            if channel_id not in user['channels']:
                raise AccessError(description=f'User u_id:{u_id} is not a member of the channel')

def check_user_owner(u_id, channel_id):
    '''
    takes a u_id and channel_id and checks if user is an owner of the channel
    returns true or false
    '''
    result = False
    for channel in channels:
        if channel_id == channel['channel_id']:
            result = u_id in channel['owner_members']

    return result


def check_channel_valid(channel_id):
    '''
    takes a channel_id and checks if it is valid
    if valid, returns index of channel in channels database (list of dictinaries)
    if invalid, raises InputError
    '''
    for i, channel in enumerate(channels):
        if channel_id == channel['channel_id']:
            return i
    else:
        raise InputError(description='Channel does not exist')


def user_flockr_owner(u_id):
    '''
    takes a u_id and checks their global permission
    returns true if user is a flockr owner
    else, returns false
    '''
    result = False
    for user in users:
        if u_id == user['u_id']:
            result = user['global_permission'] == 1

    return result


def valid_message_id(message_id):
    '''
    takes a message_id and checks if the message_id already exists
    if message_id does not exist, returns InputError
    if message_id exists, returns the channel_id it is from
    '''
    for channel in messages:
        for m in channel['messages']:
            if message_id == m['message_id']:
                return channel['channel_id']
    else:
        raise InputError(description='Message does not exist')


def message_check_user(message_id, u_id):
    '''
    takes a message_id and checks if the message_id was sent
    by the user making the request
    returns true or false
    '''
    for channel in messages:
        for m in channel['messages']:
            if message_id == m['message_id']:
                if u_id == m['u_id']:
                    return True
    else:
        return False


def change_user_reacted(messages, u_id):
    '''
    Modify `is_this_user_reacted` based on u_id
    Parameters: [{messages}], u_id
    Returns: [{messages}]
    '''
    for m in messages:
        m['reacts'][0]['is_this_user_reacted'] = u_id in m['reacts'][0]['u_ids']

    return messages

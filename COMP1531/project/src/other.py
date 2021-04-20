from itertools import chain
from data import channels, messages, users, trivias
from error import AccessError, InputError
from helper import *
from user import user_profile

##########################################################################################
###                                        CLEAR                                       ###
##########################################################################################

def clear():
    '''
    clears all data stored in database
    '''
    global users
    global channels
    global messages
    global trivias

    users.clear()
    channels.clear()
    messages.clear()
    trivias.clear()

##########################################################################################
###                                       USERS_ALL                                    ###
##########################################################################################

def users_all(token):
    '''
    Returns a list of all users and their associated details
    Parameters: token
    Return: {users}
    Exception: N/A
    '''
    get_user_id(token)

    users_list = []
    for user in users:
        u_id = user['u_id']
        users_list.append(user_profile(token, u_id)['user'])

    return {'users':users_list}

##########################################################################################
###                                ADMIN_USERPERMISSION_CHANGE                         ###
##########################################################################################

def admin_userpermission_change(token, u_id, permission_id):
    '''
    Given a User by their user ID, set their permissions to
    new permissions described by permission_id

    InputError when any of:
        - u_id does not refer to a valid user
        - permission_id does not refer to a value permission

    AccessError whenThe authorised user is not an owner
    '''

    # use get_user_id to check if token is valid, and then return back u_id
    admin_uid = get_user_id(token)
    # check if u_id of user is valid
    get_user_index(u_id)

    if permission_id not in [1, 2]:
        raise InputError(description=f'Permission id : {permission_id} invalid')

    if not user_flockr_owner(admin_uid):
        raise AccessError(description='User is not a flockr owner')

    u_index = get_user_index(u_id)
    users[u_index]['global_permission'] = permission_id
    return {}

##########################################################################################
###                                         SEARCH                                     ###
##########################################################################################

def search(token, query_str):
    '''
    Check token is valid
    Search through all channels that user is a part of,
    find message that matches query_str
    Parameters: token, query_str
    Return: {messages}
    Exceptions: N/A
    '''

    u_id = get_user_id(token)

    if query_str == '':
        return {'messages': []}

    global messages
    global users

    channel_ids = [x['channels'] for x in users if x['u_id'] == u_id][0]

    msg_list = [x['messages'] for x in messages if x['channel_id'] in channel_ids]

    msg_list_all = chain.from_iterable(msg_list) # flatten list

    results = [x for x in msg_list_all if x['message'] in query_str]

    return {'messages': change_user_reacted(results, u_id)}

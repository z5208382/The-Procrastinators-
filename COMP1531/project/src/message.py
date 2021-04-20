# pylint: disable=cyclic-import
from datetime import datetime, timezone
from threading import Timer
from data import *
from helper import *
from trivia import *

global users
global messages
global channels
global message_ids_counter

##########################################################################################
###                                 MESSAGE_SEND                                       ###
##########################################################################################
def message_send(token, channel_id, message):
    '''
    Send a message from the authorised user to the channel specified by channel_id
    Parameters: token, channel_id, message
    Return: {message_id}
    Exceptions:
        - InputError if message is more than 1000 characters
        - AccessError if the user has not joined the channel they are trying to post to
    '''
    if len(message) > 1000:
        raise InputError(description='Message exceeded 1000 characters')
    if message == '':
        return {}
    auth_id = get_user_id(token)
    check_user_in_channel(auth_id, channel_id)

    time_created = datetime.now().timestamp()
    global message_ids_counter
    message_ids_counter += 1
    for channel in messages:
        if channel['channel_id'] == channel_id:
            if message.startswith('/trivia'):
                try:
                    message = trivia_check_command(token, channel_id, message)['message']
                except InputError as e:
                    message = str(e)
            # append message to channel_message
            message_data = {
                'message_id': message_ids_counter,
                'u_id': auth_id,
                'message': message,
                'time_created': time_created,
                'reacts': [{
                    'react_id': 1,
                    'u_ids': [],
                    'is_this_user_reacted': False
                }],
                'is_pinned': False
            }
            channel['messages'].append(message_data)

    return {
        'message_id': message_ids_counter,
    }

##########################################################################################
###                                 MESSAGE_REMOVE                                     ###
##########################################################################################
def message_remove(token, message_id):
    '''
    Given a message_id, remove the corresponding message from the channel
    Parameters: token, message_id
    Return: {}
    Exceptions:
        - InputError if message_id no longer exists
        - AccessError if the message was not sent by the user making the request
        or if the user is not an owner of the channel or the flockr
    '''
    auth_id = get_user_id(token)
    channel_id = valid_message_id(message_id)
    if not (message_check_user(message_id, auth_id) or \
        check_user_owner(auth_id, channel_id) or \
        user_flockr_owner(auth_id)):
        raise AccessError(description=\
            'Message not sent by user, or user not channel or flockr owner')
    else:
        length_message = len(messages)
        for i in range(length_message):
            for message in messages[i]['messages']:
                if message_id == message['message_id']:
                    messages[i]['messages'].remove(message)
    return {}

##########################################################################################
###                                 MESSAGE_EDIT                                       ###
##########################################################################################
def message_edit(token, message_id, message):
    '''
    given a message id, the user/ owner of channel/ owner of flockr
    would be able to edit the message. If the message is empty,
    remove the message.
    Parameters: token, message_id, message
    Return: {}
    Exception: AccessError
        - message was not sent by the user making this request and
        the user is not an owner of this channel or the flockr
    '''
    global messages
    auth_id = get_user_id(token)
    channel_id = valid_message_id(message_id)
    check_user_in_channel(auth_id, channel_id)
    if not (message_check_user(message_id, auth_id) or \
        check_user_owner(auth_id, channel_id) or \
        user_flockr_owner(auth_id)):
        raise AccessError(description=\
            'Message not sent by user, or user not channel or flockr owner')

    if message == "":
        return message_remove(token, message_id)
    length_message = len(messages)
    for i in range(length_message):
        for j in range(len(messages[i]['messages'])):

            if message_id == messages[i]['messages'][j]['message_id']:

                time_created = datetime.now().replace(tzinfo=timezone.utc).timestamp()

                # update message to channel_message
                message_data = messages[i]['messages'][j]

                message_data['message'] = message
                message_data['time_created'] = time_created

                messages[i]['messages'][j] = message_data

    return {}

##########################################################################################
###                                  MESSAGE_PIN                                       ###
##########################################################################################
def message_pin(token, message_id):
    '''
    Given a message within a channel,
    mark it as "pinned" to be given special display treatment by the frontend
    Parameters:
        token, message_id
    Returns:
        {}
    Exceptions:
        InputError:
            - message_id invalid
            - message already pinned
        AccessError:
            - User not a member of channel
            - User not an owner
    '''
    u_id = get_user_id(token)

    channel_id = valid_message_id(message_id)
    check_user_in_channel(u_id, channel_id)

    if not (check_user_owner(u_id, channel_id) or user_flockr_owner(u_id)):
        raise AccessError(description='User not a flockr or channel owner')

    for msg_data in messages:
        if msg_data['channel_id'] == channel_id:
            for msg in msg_data['messages']:
                if msg['message_id'] == message_id:
                    if not msg['is_pinned']:
                        msg['is_pinned'] = True
                    else:
                        raise InputError(description='Message already pinned')
    return {}

##########################################################################################
###                                 MESSAGE_UNPIN                                      ###
##########################################################################################
def message_unpin(token, message_id):
    '''
    Given a message within a channel, remove it's mark as unpinned
    Parameters:
        token, message_id
    Returns:
        {}
    Exceptions:
        InputError:
            - message_id invalid
            - message already unpinned
        AccessError:
            - User not a member of channel
            - User not an owner
    '''
    u_id = get_user_id(token)

    channel_id = valid_message_id(message_id)
    check_user_in_channel(u_id, channel_id)

    if not (check_user_owner(u_id, channel_id) or user_flockr_owner(u_id)):
        raise AccessError(description='User not a flockr or channel owner')

    for msg_data in messages:
        if msg_data['channel_id'] == channel_id:
            for msg in msg_data['messages']:
                if msg['message_id'] == message_id:
                    if msg['is_pinned']:
                        msg['is_pinned'] = False
                    else:
                        raise InputError(description='Message already unpinned')

    return {}

##########################################################################################
###                                 MESSAGE_REACT                                      ###
##########################################################################################
def message_react(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user
    is part of, add a "react" to that particular message
    Parameters: token, message_id, react_id
    Return: {}
    Exceptions: InputError
        - message is not valid within a channel that the user has joined
        - react_id is not a valid React ID
        - message already contains an active react with react_id from the user
    '''
    u_id = get_user_id(token)

    channel_id = valid_message_id(message_id)
    check_user_in_channel(u_id, channel_id)

    if react_id not in [1]:
        raise InputError(description="Invalid react_id.")

    for msg_data in messages:
        if msg_data['channel_id'] == channel_id:
            for msg in msg_data['messages']:
                if msg['message_id'] == message_id:

                    reactions = msg['reacts'][0]
                    # Check if already reacted, otherwise add it onto database
                    if u_id in reactions['u_ids']:
                        raise InputError('Message already reacted')
                    reactions['react_id'] = react_id
                    reactions['u_ids'].append(u_id)
                    reactions['is_this_user_reacted'] = True

    return {}

##########################################################################################
###                              MESSAGE_UNREACT                                       ###
##########################################################################################
def message_unreact(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user
    is part of, add a "react" to that particular message
    Parameters: token, message_id, react_id
    Return: {}
    Exceptions: InputError
        - message is not valid within a channel that the user has joined
        - react_id is not a valid React ID
        - message does not contain an active react with react_id
    '''
    u_id = get_user_id(token)

    channel_id = valid_message_id(message_id)
    check_user_in_channel(u_id, channel_id)

    if react_id not in [1]:
        raise InputError(description="Invalid react_id.")

    for msg_data in messages:
        if msg_data['channel_id'] == channel_id:
            for msg in msg_data['messages']:
                if msg['message_id'] == message_id:

                    reactions = msg['reacts'][0]
                    # Check if already reacted, otherwise add it onto database
                    if u_id not in reactions['u_ids']:
                        raise InputError('Message already unreacted')

                    reactions['u_ids'].remove(u_id)
                    reactions['is_this_user_reacted'] = False

    return {}

##########################################################################################
###                                 MESSAGE_SENDLATER                                  ###
##########################################################################################
def message_sendlater(token, channel_id, message, time_sent):
    '''
    sending a message at a specified time in the future, which is decided by the user
    Parameters:
        token, channel_id, message, time_sent
    returns:
        {message_id}
    Exceptions:
        InputError:
            - channel_id is not valid
            - message is more than 1000 characters
            - time sent is in the past
        AccessError:
            - user is not a member of the channel
    '''
    u_id = get_user_id(token)
    check_channel_valid(channel_id)
    check_user_in_channel(u_id, channel_id)
    if len(message) > 1000:
        raise InputError(description='Message exceeded 1000 characters')

    time_sent = time_sent
    current_time = datetime.now().timestamp()
    if time_sent < current_time:
        raise InputError(description='Time is in the past. Please enter valid time')
    global message_ids_counter
    message_ids_counter += 1
    message_id = message_ids_counter

    Timer(int(time_sent - current_time), timer_send_later, [u_id, channel_id, message, \
        message_id, time_sent]).start()

    return {'message_id': message_id}

def timer_send_later(u_id, channel_id, message, message_id, time_created):
    '''
    Appends the message to channel_messages at the time_sent
    '''
    for channel in messages:
        if channel['channel_id'] == channel_id:
            # append message to channel_message
            message_data = {
                'message_id': message_id,
                'u_id': u_id,
                'message': message,
                'time_created': time_created,
                'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
                'is_pinned': False
            }
            channel['messages'].append(message_data)

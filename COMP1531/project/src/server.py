from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError
from channel import *
from auth import *
from other import *
from user import *
from message import *
from channels import *
from standup import *


def defaultHandler(err):
    '''
    created default handler
    '''
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path='/static/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)


def sanitize_input(**kwargs):
    '''
    Cast string from frontend to int
    Applicable for u_id, channel_id, start, end, message_id, etc

    !IMPORTANT: use suitable key names as it will be used
    in InputError description if any error occured

    Usage: `a, b, c = sanitize_input(a=a, b=b, c=c)`

    Parameter:
        keyword arguments
    Returns:
        Generator object / list (order of kwargs determines order of list)
    Exception:
        InputError when value passed can't be cast to int
    '''
    sanitized = []
    for key, value in kwargs.items():
        try:
            if len(kwargs.values()) == 1:
                return int(value)

            sanitized.append(int(value))
        except ValueError:
            raise InputError(description=f'{key} must be of type int')

    return sanitized


# Example
@APP.route("/echo", methods=['GET'])
def echo():
    '''
    echo route to get data
    '''
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })



##########################################################################################
###                                     AUTH ROUTES                                    ###
##########################################################################################

@APP.route("/auth/login", methods=["POST"])
def http_auth_login():
    '''
    auth_login server
    Method: POST
    Data: {email, password}
    Return: {u_id, token}
    '''
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    return dumps(auth_login(email, password))


@APP.route("/auth/logout", methods=["POST"])
def http_auth_logout():
    '''
    auth_logout server
    Method: POST
    Data: {token}
    Return: {is_success bool value}
    '''
    data = request.get_json()
    token = data.get("token")
    is_success = auth_logout(token)
    return dumps(is_success)


@APP.route('/auth/register', methods=['POST'])
def http_auth_register():
    '''
    auth_register server
    Method: POST
    Data: {email, password, name_first, name_last}
    Return: {token, u_id}
    '''
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name_first = data.get('name_first')
    name_last = data.get('name_last')
    return dumps(auth_register(email, password, name_first, name_last))

@APP.route('/auth/passwordreset/request', methods=['POST'])
def http_auth_passwordreset_request():
    '''
    auth_passwordreset_request server
    Method: POST
    Data: {email}
    Return: {}
    '''
    data = request.get_json()
    email = data.get('email')
    return dumps(auth_passwordreset_request(email))

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def http_auth_passwordreset_reset():
    '''
    auth_passwordreset_reset server
    Method: POST
    Data: {reset_code, new_password}
    Return: {}
    '''
    data = request.get_json()
    reset_code = data.get('reset_code')
    new_password = data.get('new_password')
    return dumps(auth_passwordreset_reset(reset_code, new_password))


##########################################################################################
###                                  CHANNEL ROUTES                                    ###
##########################################################################################

@APP.route('/channel/invite', methods=['POST'])
def http_channel_invite():
    '''
    channel_invite server
    Method: POST
    Data: {token, channel_id, u_id}
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    channel_id = data.get('channel_id')
    u_id = data.get('u_id')

    u_id, channel_id = sanitize_input(u_id=u_id, channel_id=channel_id)
    return dumps(channel_invite(token, channel_id, u_id))


@APP.route('/channel/details', methods=['GET'])
def http_channel_details():
    '''
    channel_details server
    Method: GET
    Data: {token, channel_id}
    Return: {name, owner_members, all_members}
    '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    channel_id = sanitize_input(channel_id=channel_id)
    return dumps(channel_details(token, channel_id))


@APP.route('/channel/messages', methods=['GET'])
def http_channel_messages():
    '''
    channel_messages
    Method: GET
    Parameters: token, channel_id, start
    Return: {messages, start, end}
    '''
    data = request.args
    token = data.get('token')
    channel_id = data.get('channel_id')
    start = data.get('start')

    channel_id, start = sanitize_input(channel_id=channel_id, start=start)
    return dumps(channel_messages(token, channel_id, start))


@APP.route('/channel/leave', methods=['POST'])
def http_channel_leave():
    '''
    channel_leave server
    Method: POST
    Data: {token, channel_id}
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    channel_id = data.get('channel_id')

    channel_id = sanitize_input(channel_id=channel_id)
    return dumps(channel_leave(token, channel_id))


@APP.route("/channel/join", methods=["POST"])
def http_channel_join():
    '''
    channel_join server
    Method: POST
    Data: {token, channel_id}
    Return: {}
    '''
    data = request.get_json()
    token = data.get("token")
    channel_id = data.get("channel_id")
    channel_id = sanitize_input(channel_id=channel_id)
    channel_join(token, channel_id)
    return dumps({}), 200


@APP.route("/channel/addowner", methods=["POST"])
def http_channel_addowner():
    '''
    channel_addowner server
    Method: POST
    Data: {token, channel_id, u_id}
    Return: {}
    '''
    data = request.get_json()
    token = data.get("token")
    channel_id = data.get("channel_id")
    u_id = data.get("u_id")
    u_id, channel_id = sanitize_input(u_id=u_id, channel_id=channel_id)
    channel_addowner(token, channel_id, u_id)
    return dumps({}), 200


@APP.route("/channel/removeowner", methods=["POST"])
def http_channel_removeowner():
    '''
    channel_removeowner server
    Method: POST
    Data: {token, channel_id, u_id}
    Return: {}
    '''
    data = request.get_json()
    token = data.get("token")
    channel_id = data.get("channel_id")
    u_id = data.get("u_id")
    u_id, channel_id = sanitize_input(u_id=u_id, channel_id=channel_id)
    channel_removeowner(token, channel_id, u_id)
    return dumps({}), 200



##########################################################################################
###                                 CHANNELS ROUTES                                    ###
##########################################################################################
@APP.route('/channels/list', methods=['GET'])
def http_channels_list():
    '''
    channels_list server
    Method: GET
    Parameter: {token}
    Return: {channels}
    '''
    token = request.args.get('token')
    return dumps(channels_list(token))


@APP.route('/channels/listall', methods=['GET'])
def http_channels_listall():
    '''
    channels_listall server
    Method: GET
    Parameter: {token}
    Return: {channels}
    '''
    token = request.args.get('token')
    return dumps(channels_listall(token))


@APP.route('/channels/create', methods=['POST'])
def http_channels_create():
    '''
    channels_create server
    Method: POST
    Parameter: {token, name, is_public}
    Return: {channel_id}
    '''
    data = request.get_json()
    token = data.get('token')
    name = data.get('name')
    is_public = data.get('is_public')
    return dumps(channels_create(token, name, is_public))

##########################################################################################
###                                 MESSAGE ROUTES                                     ###
##########################################################################################

@APP.route("/message/send", methods=['POST'])
def http_message_send():
    '''
    message_send server
    Method: POST
    Data: {token, channel_id, message}
    Return: {message_id}
    '''
    data = request.get_json()
    token = data.get('token')
    channel_id = data.get('channel_id')
    message = data.get('message')

    channel_id = sanitize_input(channel_id=channel_id)
    return dumps(message_send(token, channel_id, message))

@APP.route("/message/remove", methods=['DELETE'])
def http_message_remove():
    '''
    message_remove server
    Method: DELETE
    Data: {token, message_id}
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    message_id = data.get('message_id')

    message_id = sanitize_input(message_id=message_id)
    return dumps(message_remove(token, message_id))

@APP.route("/message/edit", methods=['PUT'])
def http_message_edit():
    '''
    message_edit server
    Method: PUT
    Data: {token, message_id, message}
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    message_id = data.get('message_id')
    message = data.get('message')

    message_id = sanitize_input(message_id=message_id)
    return dumps(message_edit(token, message_id, message))


@APP.route("/message/pin", methods=['POST'])
def http_message_pin():
    '''
    message_pin server
    Method: POST
    Data: (token, message_id)
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    message_id = data.get('message_id')
    return dumps(message_pin(token, message_id))


@APP.route("/message/unpin", methods=['POST'])
def http_message_unpin():
    '''
    message_pin server
    Method: POST
    Data: (token, message_id)
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    message_id = data.get('message_id')
    return dumps(message_unpin(token, message_id))

@APP.route("/message/sendlater", methods=['POST'])
def http_message_sendlater():
    '''
    message_sendlater server
    Method: POST
    Data: {token, channel_id, message, time_sent}
    Return: {message_id}
    '''
    data = request.get_json()
    token = data.get('token')
    channel_id = data.get('channel_id')
    message = data.get('message')
    time_sent = data.get('time_sent')

    channel_id, time_sent = sanitize_input(channel_id=channel_id, time_sent=time_sent)
    return dumps(message_sendlater(token, channel_id, message, time_sent))


@APP.route("/message/react", methods=['POST'])
def http_message_react():
    '''
    message_react server
    Method: POST
    Data = {token, message_id, react_id}
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    message_id = data.get('message_id')
    react_id = data.get('react_id')

    message_id, react_id = sanitize_input(message_id=message_id, react_id=react_id)
    return dumps(message_react(token, message_id, react_id))

@APP.route("/message/unreact", methods=['POST'])
def http_message_unreact():
    '''
    message_unreact server
    Method: POST
    Data = {token, message_id, react_id}
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    message_id = data.get('message_id')
    react_id = data.get('react_id')

    message_id, react_id = sanitize_input(message_id=message_id, react_id=react_id)
    return dumps(message_unreact(token, message_id, react_id))

##########################################################################################
###                                     USER ROUTES                                    ###
##########################################################################################

@APP.route('/user/profile', methods=['GET'])
def http_user_profile():
    '''
    user_profile server
    Method: GET
    Data: {token, u_id}
    Return: {user}
    '''
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    return dumps(user_profile(token, u_id))

@APP.route('/user/profile/setname', methods=['PUT'])
def http_user_profile_setname():
    '''
    user_profile_setname server
    Method: PUT
    Data: {token, name_first, name_last}
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    name_first = data.get('name_first')
    name_last = data.get('name_last')
    return dumps(user_profile_setname(token, name_first, name_last))


@APP.route('/user/profile/setemail', methods=['PUT'])
def http_user_profile_setemail():
    '''
    user_profile_setemail server
    Method: PUT
    Data: {token, email}
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    email = data.get('email')
    return dumps(user_profile_setemail(token, email))


@APP.route('/user/profile/sethandle', methods=['PUT'])
def http_user_profile_sethandle():
    '''
    user_profile_sethandle server
    Method: PUT
    Data: {token, handle_str}
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    handle_str = data.get('handle_str')
    return dumps(user_profile_sethandle(token, handle_str))

@APP.route("/static/<path:filename>")
def _image_server(filename):
    return send_from_directory('', filename)

@APP.route('/user/profile/uploadphoto', methods=['POST'])
def http_user_profile_uploadphoto():
    '''
    user_profile_uploadphoto server
    Method: POST
    Data: {token, img_url, x_start, y_start, x_end, y_end}
    Return: {}
    '''
    os.environ['URL'] = request.url_root
    data = request.get_json()
    token = data.get('token')
    img_url = data.get('img_url')
    x_start = data.get('x_start')
    y_start = data.get('y_start')
    x_end = data.get('x_end')
    y_end = data.get('y_end')
    x_start, y_start, x_end, y_end = sanitize_input(
        x_start=x_start, y_start=y_start,
        x_end=x_end, y_end=y_end
    )
    return dumps(user_profile_uploadphoto(
        token, img_url, x_start, y_start, x_end, y_end))

##########################################################################################
###                                    OTHER ROUTES                                    ###
##########################################################################################

@APP.route("/users/all", methods=['GET'])
def http_users_all():
    '''
    users_all server
    Method: GET
    Parameter: {token}
    Return: [{user}]
    '''
    token = request.args.get('token')
    return dumps(users_all(token))


@APP.route('/search', methods=['GET'])
def http_other_search():
    '''
    other_search server
    Method: GET
    Parameter: {token, name, is_public}
    Return: {channel_id}
    '''
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(search(token, query_str))

@APP.route("/admin/userpermission/change", methods=["POST"])
def admin_userpermission_change_route():
    '''
    Method: POST
    Parameter: {token, u_id, permission_id}
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    u_id = data.get('u_id')
    permission_id = data.get("permission_id")
    permission_id = sanitize_input(permission_id=permission_id)
    admin_userpermission_change(token, u_id, permission_id)
    return dumps({})

##########################################################################################
###                                  STANDUP ROUTES                                    ###
##########################################################################################
@APP.route("/standup/send", methods=["POST"])
def standup_send_route():
    '''
    Method: POST
    Data: token, channel_id, message
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    channel_id = data.get('channel_id')
    message = data.get('message')
    channel_id = sanitize_input(channel_id=channel_id)

    return dumps(standup_send(token, channel_id, message))

@APP.route("/standup/start", methods=["POST"])
def standup_start_route():
    '''
    Method: POST
    Data: token, channel_id, length
    Return: {}
    '''
    data = request.get_json()
    token = data.get('token')
    channel_id = data.get('channel_id')
    length = data.get('length')

    channel_id = sanitize_input(channel_id=channel_id)
    return dumps(standup_start(token, channel_id, length))


@APP.route("/standup/active", methods=["GET"])
def standup_active_route():
    '''
    Method: GET
    Parameter: token, channel_id
    Return: {}
    '''
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    channel_id = sanitize_input(channel_id=channel_id)
    return dumps(standup_active(token, channel_id))

##########################################################################################
###                                   STATIC ROUTES                                    ###
##########################################################################################

@APP.route('/static/<path:path>')
def send_js(path):
    '''
    Sends the file from the static directory to the server,
    allowing users to open the file on the frontend
    '''
    return send_from_directory('', path)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port

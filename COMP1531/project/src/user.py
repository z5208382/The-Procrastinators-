import os
import urllib.request, urllib.error
from PIL import Image
import auth
from error import InputError
from data import users
from helper import *

##########################################################################################
###                                    USER_PROFILE                                    ###
##########################################################################################
def user_profile(token, u_id):
    '''
    Returns the user's profile details
    Parameters:
        token, u_id
    Returns:
        {user}
    Exception:
        InputError:
            - user with u_id is not a valid user
    '''
    get_user_id(token)
    get_user_index(u_id)
    for user in users:
        if u_id == user['u_id']:
            user_profile = {
                'u_id'              : user['u_id'],
                'email'             : user['email'],
                'name_first'        : user['name_first'],
                'name_last'         : user['name_last'],
                'handle_str'        : user['handle'],
                'profile_img_url'   : user['profile_img_url']
            }

    return {
        'user': user_profile,
    }

##########################################################################################
###                                USER_PROFILE_SETNAME                                ###
##########################################################################################
def user_profile_setname(token, name_first, name_last):
    '''
    Update the authorised user's first and last name
    Parameters:
        token, name_first, name_last
    Returns:
        {}
    Exception:
        InputError
            - name_first is not between 1 and 50 char
            - name_last is not between 1 and 50 char

    '''
    auth_id = get_user_id(token)

    if len(name_first) > 50 or len(name_first) < 1 or \
        len(name_last) > 50 or len(name_last) < 1:
        raise InputError(description='Name is not between 1 and 50 characters')

    full_name = name_first + name_last
    for char in full_name:
        if not(char.isalpha() or char in [' ', '-']):
            raise InputError(description='Name must only contain letters, spaces or dashes')

    if not full_name.isalpha():
        raise InputError(description='Name must contain at least one letter')

    for user in users:
        if auth_id == user['u_id']:
            user['name_first'] = name_first
            user['name_last'] = name_last

    return {}


##########################################################################################
###                                USER_PROFILE_SETEMAIL                               ###
##########################################################################################
def user_profile_setemail(token, email):
    '''
    Update authorised user's email address
    Parameters:
        token, email
    Returns:
        {}
    Exception:
        InputError
            - Invalid email format
            - Email already in use
    '''
    u_id = get_user_id(token)

    email = auth.is_valid_email(email)

    global users

    if email in [user['email'] for user in users]:
        raise InputError(description='Email is being used by another user')

    for user in users:
        if user['u_id'] == u_id:
            user['email'] = email

    return {}


##########################################################################################
###                             USER_PROFILE_SETHANDLE                                 ###
##########################################################################################
def user_profile_sethandle(token, handle_str):
    '''
    Update authorised user's handle (display name)
    Parameters:
        token, handle_str
    Returns:
        {}
    Exception:
        InputError
            - handle_str not in between 3 and 20 chars
            - handle_str already in use
    '''
    u_id = get_user_id(token)

    if not 3 <= len(handle_str) <= 20:
        raise InputError(description=f'Handle length of {len(handle_str)} \
            is not between 3 and 20 characters long')

    global users
    if handle_str in [user['handle'] for user in users]:
        raise InputError(description=f'Handle {handle_str} is already in use')

    for user in users:
        if user['u_id'] == u_id:
            user['handle'] = handle_str

    return {}

##########################################################################################
###                             USER_UPLOAD_PROFILE                                    ###
##########################################################################################
def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Allows the user to upload a image from a URL, and crops that image
    accoridng to x and y values.
    Parameters:
        - token     : the user's token
        - img_url   : the URL of the image
        - x_start   : the start of the crop in x axis, where top left is (0,0)
        - y_start   : the start of the crop in y axis, where top left is (0,0)
        - x_end     : the end of the crop in x axis, where top left is (0,0)
        - y_end     : the end of the crop in y axis, where top left is (0,0)
    Returns:
        {}
    '''
    u_id = get_user_id(token)

    img_path = './src/static/tmp.jpg'
    try:
        urllib.request.urlopen(img_url)
    except urllib.error.HTTPError as e:
        raise InputError(description='HTTPError: {}'.format(e.code))

    urllib.request.urlretrieve(img_url, img_path)
    image_object = Image.open(img_path)

    if image_object.format != 'JPEG':
        raise InputError(description="Not JPG image uploaded")

    width, height = image_object.size
    if x_end > width:
        raise InputError(description='cropping width is greater than image width')

    if y_end > height:
        raise InputError(description='cropping height is greater than image height')

    if x_start < 0 or y_start < 0:
        raise InputError(description='start is out of bounds')

    cropped = image_object.crop((x_start, y_start, x_end, y_end))
    img_path = f'./src/static/profile_{u_id}.jpg'
    cropped.save(img_path)

    url = os.environ['URL']

    for user in users:
        if u_id == user['u_id']:
            user['profile_img_url'] = f'{url}static/profile_{u_id}.jpg'

    return {}

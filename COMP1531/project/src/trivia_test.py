import time
import random
import pytest
from trivia import *
from error import *
from helper_tests import (
    create_public_channel,
    register
)
from auth import auth_logout
from other import clear
from channel import channel_messages, channel_join
from message import *

##########################################################################################
###                                 TRIVIA_START TESTS                                 ###
##########################################################################################
def test_trivia_start_invalid_token():
    '''
    Test 1: Invalid token when starting trivia
    Expect an AccessError
    '''
    clear()
    _, token = register('Hello')
    channel = create_public_channel(token, 'OKAY')
    auth_logout(token)
    with pytest.raises(AccessError):
        trivia_start(token, channel, 'default_UNSW')


def test_trivia_start_invalid_channel_id():
    '''
    Test 2: Invalid channel id when starting trivia
    Expect InputError
    '''
    clear()
    _, token = register('Hello')
    channel = create_public_channel(token, 'OKAY')
    with pytest.raises(InputError):
        trivia_start(token, channel + 100, 'default_UNSW')


def test_trivia_start_invalid_category_name():
    '''
    Test 3: Category name does not exist
    Expect InputError
    '''
    clear()
    _, token = register('Hello')
    channel = create_public_channel(token, 'OKAY')
    with pytest.raises(InputError):
        trivia_start(token, channel, 'not-a-category')


def test_trivia_start_category_no_questions():
    '''
    Test 4: Category has no questions
    Expect InputError
    '''
    clear()
    _, token = register('Hello')
    channel = create_public_channel(token, 'OKAY')
    name = 'comp1531'
    trivia_create(token, channel, name)
    with pytest.raises(InputError):
        trivia_start(token, channel, name)


def test_trivia_start_already_started():
    '''
    Test 5: Trivia has already started
    Expect InputError
    '''
    clear()
    _, token = register('Hello')
    channel = create_public_channel(token, 'OKAY')
    trivia_start(token, channel, 'default_UNSW')
    with pytest.raises(InputError):
        trivia_start(token, channel, 'default_UNSW')
    time.sleep(0.1)
    trivia_end(token, channel, 'default_UNSW')


def test_trivia_valid():
    '''
    Test 6: Normal trivia game starting, and ending
    This should work
    '''
    clear()
    _, token = register('Hello')
    channel = create_public_channel(token, 'OKAY')
    trivia_start(token, channel, 'default_UNSW')
    time.sleep(0.1)
    trivia_end(token, channel, 'default_UNSW')


def test_trivia_multi_channel_valid():
    '''
    Test 7: Normal trivia game starting in multiple channel
    and ending
    This should work
    '''
    clear()
    _, token = register('Hello')
    channels = [create_public_channel(token, a) for a in "ABCDE"]
    [trivia_start(token, channel, 'default_UNSW') for channel in channels]
    time.sleep(0.1)
    channels.reverse()
    [trivia_end(token, channel, 'default_UNSW') for channel in channels]

##########################################################################################
###                                  TRIVIA_END TESTS                                  ###
##########################################################################################
def test_trivia_end_invalid_token():
    '''
    Test 1: Invalid token when ending trivia
    Expect an AccessError
    '''
    clear()
    _, token = register('Hello')
    channel = create_public_channel(token, 'OKAY')
    trivia_start(token, channel, 'default_UNSW')
    with pytest.raises(AccessError):
        trivia_end(token + 'a', channel, 'default_UNSW')
    time.sleep(0.1)
    trivia_end(token, channel, 'default_UNSW')


def test_trivia_end_invalid_channel():
    '''
    Test 2: Invalid channel id when ending trivia
    Expect InputError
    '''
    clear()
    _, token = register('Hello')
    channel = create_public_channel(token, 'OKAY')
    trivia_start(token, channel, 'default_UNSW')
    with pytest.raises(InputError):
        trivia_end(token, channel + 100, 'default_UNSW')
    time.sleep(0.1)
    trivia_end(token, channel, 'default_UNSW')


def test_trivia_end_invalid_category():
    '''
    Test 3: Trivia ended, but category name does not exist
    Expect InputError
    '''
    clear()
    _, token = register('Hello')
    channel = create_public_channel(token, 'OKAY')
    trivia_start(token, channel, 'default_UNSW')
    time.sleep(0.1)
    with pytest.raises(InputError):
        trivia_end(token, channel, 'not-a-category')
    time.sleep(0.1)
    trivia_end(token, channel, 'default_UNSW')


def test_trivia_end_no_trivia_active():
    '''
    Test 4: End trivia when no trivia is on going
    Expect InputError
    '''
    clear()
    _, token = register('Hello')
    channel = create_public_channel(token, 'OKAY')
    with pytest.raises(InputError):
        trivia_end(token, channel, 'default_UNSW')


def test_trivia_start_end_automatic():
    '''
    Test 5: Start trivia, play till trivia ends
    Call trivia end and expect InputError
        Player 1 is a good person,
        but Player 2 always cheats by choosing 2 everytime
    '''
    clear()
    _, player_1 = register('Hello')
    _, player_2 = register('Hiiii') # player 2 is a cheater >_<
    channel = create_public_channel(player_1, 'OKAY')
    channel_join(player_2, channel)

    trivia_start(player_1, channel, 'default_UNSW')
    start_idx = 0
    for end_idx in range(5, 6 * (4 + 1), 5): # 5 questions x (4 options + 1 question prompt)
        time.sleep(1.5)

        messages = channel_messages(player_1, channel, 0)['messages']
        messages.reverse()
        options = messages[start_idx + 1: end_idx]
        choice = random.choice(options)
        message_react(player_1, choice['message_id'], 1)

        messages = channel_messages(player_2, channel, 0)['messages']
        messages.reverse()
        options = messages[start_idx + 1: end_idx]
        random.shuffle(options)
        choice = options.pop()
        message_react(player_2, choice['message_id'], 1)
        choice = options.pop()
        message_react(player_2, choice['message_id'], 1)

        start_idx = end_idx
        time.sleep(8.5)

    while threading.active_count() > 1:
        pass

    with pytest.raises(InputError):
        trivia_end(player_1, channel, 'default_UNSW')

    leaderboard = channel_messages(player_1, channel, 0)['messages'][0]['message']
    assert leaderboard.startswith("Trivia ended!\nLeaderboard:\n\t")


###############################################################
###             TRIVIA_CHECK_COMMAND TESTS                  ###
###############################################################

def test_check_command_input_error():
    '''
    Test 1: message given does not match any command
    InputError is raised
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    with pytest.raises(InputError):
        trivia_check_command(token, channel_id, "/trivia invalid_command")

def test_check_command_trivia():
    '''
    Test 2: '/trivia' with no following commands
    shows the categories and commands available
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message = trivia_instructions(channel_id)['message']
    message_check = trivia_check_command(token, channel_id, "/trivia")['message']
    assert message == message_check

def test_check_command_instructions():
    '''
    Test 3: '/trivia ?' shows the categories and commands
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message = trivia_instructions(channel_id)['message']
    message_check = trivia_check_command(token, channel_id, "/trivia ?")['message']
    assert message == message_check

def test_check_command_incorrect_trivia():
    '''
    Test 4: /trivia is not correctly called
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    with pytest.raises(InputError):
        trivia_check_command(token, channel_id, "/triviaaa")

def test_check_command_create():
    '''
    Test 5: '/trivia create <name of new category>'
    a new category is created
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    trivia_check_command(token, channel_id, "/trivia create new_category")
    message = trivia_check_command(token, channel_id, "/trivia ?")['message']
    assert "new_category" in message

def test_check_command_create_incorrect():
    '''
    Test 6: /trivia create is input with no category name
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    with pytest.raises(InputError):
        trivia_check_command(token, channel_id, "/trivia create")

def test_check_command_add_questions():
    '''
    Test 7: '/trivia add_questions <name of category>'
    add questions and their options to the given category
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    trivia_create(token, channel_id, "new_category")
    question = "/trivia add_questions new_category\n" + \
        "Random question?\nYes\nNo"
    message = trivia_check_command(token, channel_id, question)['message']
    assert message == "Question Successfully Added"

def test_check_command_add_questions_incorrect():
    '''
    Test 8: /trivia add_questions is called without a new category or questions
    to add
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    with pytest.raises(InputError):
        trivia_check_command(token, channel_id, "/trivia add_questions")

def test_check_command_add_questions_incorrect_questions():
    '''
    Test 9: /trivia add_questions is called without questions to add
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    trivia_create(token, channel_id, "new_category")
    question = "/trivia add_questions new_category"
    with pytest.raises(InputError):
        trivia_check_command(token, channel_id, question)

def test_check_command_start():
    '''
    Test 10: '/trivia start <name of category>'
    start the trivia category given
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message = trivia_check_command(token, channel_id, "/trivia start default_UNSW")['message']
    assert message == "Trivia started! React to your chosen option!"
    trivia_end(token, channel_id, "default_UNSW")

def test_check_command_start_incorrect():
    '''
    Test 11: /trivia start is called without a category name
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    with pytest.raises(InputError):
        trivia_check_command(token, channel_id, "/trivia start")

def test_check_command_end():
    '''
    Test 12: '/trivia end'
    trivia game is ended
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    trivia_start(token, channel_id, "default_UNSW")
    trivia_check_command(token, channel_id, "/trivia end")
    with pytest.raises(InputError):
        trivia_end(token, channel_id, "default_UNSW")

def test_trivia_create_invalid_end_channelid():
    '''
    Test 13: If an invalid channel_id is input
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    dummy = create_public_channel(token, '2')
    trivia_start(token, channel_id, "default_UNSW")
    with pytest.raises(InputError):
        trivia_check_command(token, dummy, "/trivia end")
    trivia_end(token, channel_id, "default_UNSW")

def test_check_command_time():
    '''
    Test 14: '/trivia time'
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message = trivia_check_command(token, channel_id, "/trivia time 5")['message']
    assert message == "Time limit has been changed succesfully"

def test_check_command_time_incorrect():
    '''
    Test 15: /trivia time is called without a time limit
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    with pytest.raises(InputError):
        trivia_check_command(token, channel_id, "/trivia time")

###############################################################
###              TRIVIA_INSTRUCTIONS TESTS                  ###
###############################################################
def test_instructions_default():
    '''
    Test 1: instructions with the default trivia category
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message = trivia_instructions(channel_id)['message']
    assert message == \
    " ******** TRIVIA ******** \n\n" + \
    "CATEGORIES:\n" + \
    "default_UNSW\n\n" + \
    "COMMANDS:\n" + \
    "View categories and commands: /trivia ?\n" + \
    "Create a new category: /trivia create <cateogry_name>\n" + \
    "Add questions to a category: /trivia add_questions <name of category>\\n" + \
            "<question>\\n<max 4 options each on a new line>\n" + \
    "Start playing a category: /trivia start <name of category>\n" + \
    "End a game: /trivia end\n" + \
    "Change the time limit for each question: /trivia time <seconds>"


def test_instructions_add_category():
    '''
    Test 2: list of categories are updated with new category
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    trivia_create(token, channel_id, "new_category")
    message = trivia_instructions(channel_id)['message']
    assert "new_category" in message

def test_instructions_multiple_channels():
    '''
    Test 3: list of categories are different depending on channel
    '''
    clear()
    token = register('1')[1]
    channel_ids = []
    names = ["category 1", "category 2", "category 3"]
    for i in range(3):
        channel_ids.append(create_public_channel(token, str(i)))
        trivia_create(token, channel_ids[i], names[i])

    messages = []
    for channel_id in channel_ids:
        messages.append(trivia_instructions(channel_id)['message'])
    assert "category 1" in messages[0]
    assert ("category 2" and "category 3") not in messages[0]
    assert "category 2" in messages[1]
    assert ("category 1" and "category 3") not in messages[1]
    assert "category 3" in messages[2]
    assert ("category 1" and "category 2") not in messages[2]


##########################################################################################
###                             TRIVIA_ADD_QUESTIONS TESTS                             ###
##########################################################################################

def test_trivia_add_questions_invalid_channelid():
    '''
    Test 1: Invalid channel_id entered
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    dummy = create_public_channel(token, '2')
    name = 'new_category'
    question = "Random question?\nYes\nNo"
    trivia_create(token, channel_id, name)
    trivia_create(token, dummy, name)

    with pytest.raises(InputError):
        trivia_add_questions(token, dummy, 'invalid_category', question)

def test_invalid_category_entered():
    '''
    Test 2: Invalid catogory name entered
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')

    name = 'new_category'
    trivia_create(token, channel_id, name)

    name = 'invalid_category'
    question = "Random question?\nYes\nNo"

    with pytest.raises(InputError):
        trivia_add_questions(token, channel_id, name, question)

def test_message_not_split():
    '''
    Test 3: The message given to add_questions is not split into new lines
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')

    name = 'new_category'
    trivia_create(token, channel_id, name)

    question = "Random question?123"

    with pytest.raises(InputError):
        trivia_add_questions(token, channel_id, name, question)

def test_only_question_entered():
    '''
    Test 4: Only 1 question entered in message
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')

    name = 'new_category'
    trivia_create(token, channel_id, name)

    question = "Random question?"

    with pytest.raises(InputError):
        trivia_add_questions(token, channel_id, name, question)

def test_only_one_option():
    '''
    Test 5: Only 1 option with question entered in message
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')

    name = 'new_category'
    trivia_create(token, channel_id, name)

    question = "Random question?\nYes"

    with pytest.raises(InputError):
        trivia_add_questions(token, channel_id, name, question)

def test_more_than_four_options():
    '''
    Test 6: Greater than 4 options entered with question in message
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')

    name = 'new_category'
    trivia_create(token, channel_id, name)

    question = "Random question?\n1\n2\n3\n4\n5"

    with pytest.raises(InputError):
        trivia_add_questions(token, channel_id, name, question)

    question = "Random question?\n1\n2\n3\n4\n5\n6\n7\n8"

    with pytest.raises(InputError):
        trivia_add_questions(token, channel_id, name, question)

def test_valid_add_questions():
    '''
    Test 7: User validly adds a question to the trivia
    Program should print "Question added successfully"
    '''
    clear()
    token = register('1')[1]
    create_public_channel(token, '1')
    channel_id = create_public_channel(token, '2')

    name = 'new_category'
    trivia_create(token, channel_id, name)

    question = "Random question?\n1\n2\n3"

    # Check return value to see if successful message sent
    assert trivia_add_questions(token, channel_id, name, question)['message'] ==\
    "Question Successfully Added"

def test_addquestion_defaultUNSW():
    '''
    Test 8: Ensure you can add questions to default UNSW category as well
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    question = "Random question?\n1\n2\n3"
    # Check return value to see if successful message sent
    assert trivia_add_questions(token, channel_id, 'default_UNSW', question)\
    ['message'] == "Question Successfully Added"

##########################################################################################
###                                 TRIVIA_CREATE TESTS                                ###
##########################################################################################

def test_trivia_create_invalid_token():
    '''
    Test 1: If an invalid token is input
    Raise AccessError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    auth_logout(token)

    with pytest.raises(AccessError):
        trivia_create(token, channel_id, 'UNSW')

def test_trivia_create_invalid_channelid():
    '''
    Test 2: If an invalid channel_id is input
    Raise InputError
    '''
    clear()
    token = register('1')[1]

    with pytest.raises(InputError):
        trivia_create(token, 1, 'UNSW')

def test_trivia_name_exceeds_fifty():
    '''
    Test 3: If the category name being input exceeds 50 characters
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')

    with pytest.raises(InputError):
        trivia_create(token, channel_id, 'x'*51)

def test_trivia_name_exists():
    '''
    Test 4: If the category name being input already exists
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    trivia_create(token, channel_id, 'UNSW')

    with pytest.raises(InputError):
        trivia_create(token, channel_id, 'UNSW')

def test_trivia_create_valid():
    '''
    Test 5: Check that a category can be created successfully
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')

    assert trivia_create(token, channel_id, 'UNSW')['message'] ==\
    "Category: UNSW has been succesfully created\nTo add questions please type" +\
    " /trivia and follow the command for adding questions"

def test_trivia_create_multiple():
    '''
    Test 6: Check that multiple different categories can be created successfully
    by different users
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')

    assert trivia_create(token1, channel_id, 'UNSW')['message'] ==\
    "Category: UNSW has been succesfully created\nTo add questions please type" +\
    " /trivia and follow the command for adding questions"

    assert trivia_create(token2, channel_id, 'USYD')['message'] ==\
    "Category: USYD has been succesfully created\nTo add questions please type" +\
    " /trivia and follow the command for adding questions"

def test_trivia_create_different_channels():
    '''
    Test 7: Check that trivia categories with the same name can be created in
    different channels
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id1 = create_public_channel(token1, '1')
    channel_id2 = create_public_channel(token2, '2')

    assert trivia_create(token1, channel_id1, 'UNSW')['message'] ==\
    "Category: UNSW has been succesfully created\nTo add questions please type" +\
    " /trivia and follow the command for adding questions"

    assert trivia_create(token2, channel_id2, 'UNSW')['message'] ==\
    "Category: UNSW has been succesfully created\nTo add questions please type" +\
    " /trivia and follow the command for adding questions"

##########################################################################################
###                                 TRIVIA_TIME TESTS                                  ###
##########################################################################################

def test_trivia_time_invalid_channelid():
    '''
    Test 1: If an invalid channel_id is input
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    time_limit = 10
    with pytest.raises(InputError):
        trivia_time(token, channel_id + 100, time_limit)

def test_invalid_token():
    '''
    Test 2: tests for invalid token
    raise AccessError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    time_limit = 10
    auth_logout(token)
    with pytest.raises(AccessError):
        trivia_time(token, channel_id, time_limit)

def test_time_limit_not_5s():
    '''
    Test 3: The time limit is not a multiple of 5
    Raises an InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    time_limit = 13
    with pytest.raises(InputError):
        trivia_time(token, channel_id, time_limit)

def test_time_limit_too_small():
    '''
    Test 4: The time limit is less than 5 seconds
    Raises an InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    time_limit = 3
    with pytest.raises(InputError):
        trivia_time(token, channel_id, time_limit)

def test_time_limit_too_large():
    '''
    Test 5: The time limit is greater than 20 seconds
    Raises an InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    time_limit = 30
    with pytest.raises(InputError):
        trivia_time(token, channel_id, time_limit)

def test_time_limit_valid():
    '''
    Test 6: The time limit is valid number
    Raises an InputError
    '''
    clear()
    token = register('1')[1]
    create_public_channel(token, '1')
    channel_id = create_public_channel(token, '2')
    time_limit = 15
    assert trivia_time(token, channel_id, time_limit) ==\
    {'message': "Time limit has been changed succesfully"}

# pylint: disable=cyclic-import
import random
import threading
import time
from collections import Counter, OrderedDict
from itertools import accumulate
import message as _msg
from data import messages, trivias, users
from error import InputError
from helper import *

################################################################################################
###                              TRIVIA_CHECK_COMMAND                                        ###
################################################################################################
def trivia_check_command(token, channel_id, message):
    '''
    Checks the message that starts with /trivia and calls
    the function corresponding with the command
    Exceptions: InputError - invalid format or command
    Returns: {message}
    '''
    command_format = {
        "instructions": "/trivia",
        "create": "/trivia create <cateogry_name>",
        "add_questions": "/trivia add_questions <name of category>\\n" + \
            "<question>\\n<max 4 options each on a new line>",
        "start": "/trivia start <name of category>",
        "end": "/trivia end <name",
        "time": "/trivia time <seconds>"
        }
    message = message.split(' ')
    message_len = len(message)

    if message[0] != "/trivia":
        raise InputError(description=f"invalid format: {command_format['instructions']}")
    if message_len == 1 or message[1] == "?":
        return_message = trivia_instructions(channel_id)['message']

    elif message[1] == "create":
        if message_len > 2:
            name = (' ').join(message[2:])
            return_message = trivia_create(token, channel_id, name)['message']
        else:
            raise InputError(description=f"invalid format: {command_format['create']}")

    elif message[1] == "add_questions":
        if message_len > 2:
            message = (' ').join(message[2:])
            message = message.split('\n')
            if len(message) > 1:
                category_name = message[0]
                return_message = trivia_add_questions(token, channel_id, category_name, \
                    ('\n').join(message[1:]))['message']
            else:
                raise InputError(description=f"invalid format: {command_format['add_questions']}")
        else:
            raise InputError(description=f"invalid format: {command_format['add_questions']}")

    elif message[1] == "start":
        if message_len > 2:
            name = (' ').join(message[2:])
            return_message = trivia_start(token, channel_id, name)['message']
        else:
            raise InputError(description=f"invalid format: {command_format['start']}")

    elif message[1] == "end":
        for trivia in trivias:
            if channel_id == trivia['channel_id']:
                category_name = trivia['current_category']
                if category_name is None:
                    raise InputError(description="Current category not found")

        return_message = trivia_end(token, channel_id, category_name)['message']

    elif message[1] == "time":
        if message_len > 2:
            return_message = trivia_time(token, channel_id, int(message[2]))['message']
        else:
            raise InputError(description=f"invalid format: {command_format['time']}")

    else:
        raise InputError(description="Invalid format. " + \
            "Type /trivia to see the commands available.")

    return {'message': return_message}

################################################################################################
###                                    TRIVIA/START                                          ###
################################################################################################
def trivia_start(token, channel_id, category_name):
    '''
    Starts a trivia session
    Parameters: token, channel_id, category_name
    Returns: None
    Exception, InputError:
        - Trivia start called when trivia is already running
        - Category chosen has no questions
        - Category does not exist
        - Channel id invalid
    '''
    get_user_id(token)
    category = None

    global trivias
    for trivia in trivias:
        if channel_id == trivia['channel_id']:
            if trivia['trivia_active']:
                raise InputError(description='Trivia is already running')

            time_limit = trivia['time_limit']

            # cat as in 'category'
            for cat in trivia['categories']:
                if category_name == cat['name']:
                    if cat['questions'] == []:
                        raise InputError(description=f'Category {category_name} has no questions')
                    else:
                        category = cat
                        break
            else:
                raise InputError(description='Category does not exist')

        if category is not None:
            break

    else:
        raise InputError(description='Invalid channel id')

    user = {
        'token': token,
        'channel_id': channel_id
    }
    t = threading.Thread(
        target=queue_questions,
        args=(time_limit, user, category['questions'], category['name'])
    )
    for trivia in trivias:
        if trivia['channel_id'] == channel_id:
            trivia['thread'] = t
            trivia['trivia_active'] = True
            trivia['current_category'] = category_name

    t.start()

    return {'message': 'Trivia started! React to your chosen option!'}

def queue_questions(interval, user, question_list, category_name):
    '''
    Puts questions in a queue, checks trivia_active, if False, loop breaks
    Between each questions,
        it stops until either:
            interval has passed
            or
            trivia_active is False
    '''
    global trivias
    token = user['token']
    channel = user['channel_id']
    questions = list(question_list)
    msg_ids = []
    running = True
    time.sleep(0.3)
    while running:
        try:
            q = questions.pop()
        except IndexError:
            results = trivia_end(token, channel, category_name)
            _msg.message_send(token, channel, results['message'])
            break

        message = f"TRIVIA:\n\t{q['question']}"
        _msg.message_send(token, channel, message)
        time.sleep(0.2)

        options = list(q['options'])
        random.shuffle(options)
        for opts in options:
            opts = f"TRIVIA (option):\n\t{opts}"
            msg_id = _msg.message_send(token, channel, opts)['message_id']
            msg_ids.append(msg_id)

        for triv in trivias: # pragma: no branch
            if triv['channel_id'] == channel:
                triv['msg_ids'] = msg_ids
                break

        end_time = time.time() + interval
        wait = True
        while wait:
            current_time = time.time()
            for trivia in trivias:
                if trivia['channel_id'] == channel and not trivia['trivia_active']:
                    running = False
                    wait = False
                    break
            if current_time >= end_time:
                break

################################################################################################
###                                     TRIVIA/END                                           ###
################################################################################################
def trivia_end(token, channel_id, category_name):
    '''
    End a currently running trivia.
    Displays scoreboard of users participating.
    Parameters: token, channel_id, category_name
    Returns: None
    Exception, InputError:
        - Trivia end called when no trivia is running
        - Category does not exist
        - Channel id not found
    '''
    get_user_id(token)
    global trivias
    for trivia in trivias:
        if trivia['channel_id'] == channel_id:
            if not trivia['trivia_active']:
                raise InputError(description='No trivia running')
            else:
                for cat in trivia['categories']:
                    if cat['name'] == category_name:
                        questions = cat['questions']
                        break
                else:
                    raise InputError(description="Category not found")

                trivia['trivia_active'] = False
                trivia['current_category'] = None
                msg_ids = trivia['msg_ids']

                break
    else:
        raise InputError(description="Channel not found")

    global messages
    all_msg = None
    for msg in messages:
        if msg['channel_id'] == channel_id:
            all_msg = msg['messages']

    triv_opts = [msg for msg in all_msg if msg['message_id'] in msg_ids]

    # Assume first option is correct
    corrects = [q['options'][0] for q in questions]

    points = Counter()
    for ans in _get_answers(triv_opts, corrects):
        for u_id in ans['reacts'][0]['u_ids']:
            u_id = str(u_id)
            points[u_id] += 1

    for cheater in _get_cheaters(questions, triv_opts):
        u_id = str(cheater)
        points[u_id] = 0

    final_score = {_get_handle_from_id(int(u_id)):score for u_id, score in points.items()}
    final_score = OrderedDict(sorted(final_score.items(), key=lambda x: x[1], reverse=True))

    score_text = ""
    for handle, score in final_score.items():
        score_text += f"\t{handle}: {score}\n"

    return {'message': f'Trivia ended!\nLeaderboard:\n{score_text}'}


##########################################################################################
###                              'static' helper functions                             ###
##########################################################################################
def _get_cheaters(questions, triv_opts):
    cheaters = set()
    opt_lengths = [len(x['options']) for x in questions]
    end_indexes = list(accumulate(opt_lengths))

    start_idx = 0
    for end_idx in end_indexes:
        frame = [x['reacts'][0]['u_ids'] for x in triv_opts[start_idx:end_idx]]
        start_idx = end_idx

        if frame == []:
            continue  # no reacts

        opt_ids = []
        for question_u_ids in frame:
            opt_ids += question_u_ids

        uniq = set()
        for opt_id in opt_ids:
            if opt_id not in uniq:
                uniq.add(opt_id)
            else:
                cheaters.add(opt_id)

    return cheaters


def _get_answers(triv_opts, corrects):
    answers = []
    for opt in triv_opts:
        if opt['message'].split('(option):\n\t')[1] in corrects:
            answers.append(opt)

    return answers


def _get_handle_from_id(u_id):
    global users
    for user in users: # pragma: no branch
        if u_id == user['u_id']:
            return user['handle']



################################################################################################
###                                TRIVIA/INSTRUCTIONS                                       ###
################################################################################################
def trivia_instructions(channel_id):
    '''
    Returns a message containing the available categories and commands
    Returns: {message}
    '''
    command_format = {
        "instructions": "/trivia ?",
        "create": "/trivia create <cateogry_name>",
        "add_questions": "/trivia add_questions <name of category>\\n" + \
            "<question>\\n<max 4 options each on a new line>",
        "start": "/trivia start <name of category>",
        "end": "/trivia end",
        "time": "/trivia time <seconds>"
        }
    global trivias
    message_categories = ["CATEGORIES:"]
    for channel in trivias:
        if channel_id == channel['channel_id']:
            for category in channel['categories']:
                message_categories.append(category['name'])

    message_categories = ('\n').join(message_categories)
    commands = ["COMMANDS:", f"View categories and commands: {command_format['instructions']}", \
        f"Create a new category: {command_format['create']}", \
        f"Add questions to a category: {command_format['add_questions']}", \
        f"Start playing a category: {command_format['start']}", \
        f"End a game: {command_format['end']}", \
        f"Change the time limit for each question: {command_format['time']}"]
    commands = ('\n').join(commands)

    message = [" ******** TRIVIA ******** ", message_categories, commands]
    message = ('\n\n').join(message)
    return {'message': message}


################################################################################################
###                                  TRIVIA/ADD_QUESTIONS                                    ###
################################################################################################

def trivia_add_questions(token, channel_id, category_name, message):
    '''
    Allows user to add questions to a category. User inputs question
    and options between 2 to 4 only and the options are each followed by a new line
    Input Error:
        - options provided less than 2 or greater than 4
        - Category name does not exist
    '''
    u_id = get_user_id(token)
    check_channel_valid(channel_id)
    check_user_in_channel(u_id, channel_id)

    instruction_description = "Please enter questions in the following format:\n" + \
            "/trivia add_questions <name of category>\\n" + \
            "<question>\\n<max 4 options each on a new line>"

    message = message.split('\n')

    # message must have 1 question and at least 2 options
    if len(message) > 2 and len(message) < 6:
        check_valid_category(channel_id, category_name)
        set_question_options(channel_id, category_name, message)
        return {"message": "Question Successfully Added"}
    else:
        raise InputError(description=instruction_description)

def check_valid_category(channel_id, category_name):
    '''
    Checks if valid category name given
    '''
    for trivia in trivias: # pragma: no branch
        if channel_id == trivia['channel_id']:

            for category in trivia['categories']:
                if category['name'] == category_name:
                    return True
            else:
                raise InputError(description='Invalid category name')

def set_question_options(channel_id, category_name, message):
    '''
    Append question, correct option and shuffled options list to
    trivia category dictionary in database
    '''
    options = []

    for trivia in trivias:
        if channel_id == trivia['channel_id']:
            for category in trivia['categories']:
                if category['name'] == category_name:
                    question_dictionary = {}
                    question = message[0]
                    options = message[1:]
                    # random.shuffle(options)
                    question_dictionary['question'] = question
                    # question_dictionary['correct_option'] = message[1]
                    question_dictionary['options'] = options
                    category['questions'].append(question_dictionary)

################################################################################################
###                                        TRIVIA/TIME                                       ###
################################################################################################

def trivia_time(token, channel_id, time_limit):
    '''
    Sets the time per trivia question
    Parameters: token, channel_id, time_limit
    Returns: None
    Exceptions:
        InputError:
        - time_limit not a multiple of 5 seconds
        - time_limit not between 5 and 20 seconds
        AccessError:
        - Invalid token is input
    '''
    global trivias
    u_id = get_user_id(token)
    check_channel_valid(channel_id)
    check_user_in_channel(u_id, channel_id)

    if time_limit % 5 != 0:
        raise InputError(description='Time given is not a multiple of 5 seconds')
    if time_limit < 5 or time_limit > 20:
        raise InputError(description='Time given is not between 5 and 20 seconds')

    for trivia in trivias:
        if channel_id == trivia['channel_id']:
            trivia['time_limit'] = time_limit
    return {'message': "Time limit has been changed succesfully"}

################################################################################################
###                                  TRIVIA/CREATE                                           ###
################################################################################################

def trivia_create(token, channel_id, name):
    '''
    Creates a category name
    Parameters: token, channel_id, category_name
    Returns: None
    Exceptions:
        InputError:
        - name exceeds 50 characters
        - name already exists
        - channel_id is invalid
        AccessError:
        - Invalid token is input
    '''
    get_user_id(token)
    check_channel_valid(channel_id)

    if len(name) > 50:
        raise InputError(description=f"Category name {name} is invalid" +\
        " (length is greater than 50 characters)")

    for trivia in trivias:
        if channel_id == trivia['channel_id']:
            for category in trivia['categories']:
                if category['name'] == name:
                    raise InputError(description=f"Category name {name} already exists")
            new_category = {}
            new_category['name'] = name
            new_category['questions'] = []
            trivia['categories'].append(new_category)
            message = f"Category: {name} has been succesfully created\n" + \
                "To add questions please type /trivia and follow the command for adding questions"

    return {"message": message}

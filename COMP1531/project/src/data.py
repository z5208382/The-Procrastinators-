'''
Implementation for database
'''

users = []
channels = []
messages = []
trivias = []
message_ids_counter = 0

##########################################################################################
###                                   USERS_DATA_STRUCTURE                             ###
##########################################################################################

# users = [
#     {
#         'u_id' : u_id,
#         'token' : token,
#         'password' : password,
#         'name_first' : name_first,
#         'name_last' : name_last,
#         'email' : email,
#         'handle' : handle_str,
#         'img_url': profile_img_url
#         'channels' : [channel_id],
#         'global_permission': permission_id
#     }
# ]

##########################################################################################
###                                  CHANNELS_DATA_STRUCTURE                           ###
##########################################################################################

# channels = [
#     {
#         'channel_id' : channel_id,
#         'is_public' : is_public,
#         'name' : channel_name,
#         'owner_members' : [u_id],
#         'all_members' : [u_id],
#         'standup': time_finish
#     }
# ]


##########################################################################################
###                                  MESSAGES_DATA_STRUCTURE                           ###
##########################################################################################

# messages = [
#     {
#         'channel_id': channel_id,
#         'messages': [
#             {   'message_id': message_id,
#                 'u_id': u_id,
#                 'message': " ",
#                 'time_created': datetime()
#                 'reacts':{ react_id: 1, u_ids: [], is_this_user_reacted: Boolean }
#                 'is_pinned': Boolean
#             },
#         'standup_messages': " ",
#     }
#         ]

##########################################################################################
###                                  TRIVIA_DATA_STRUCTURE                            ###
##########################################################################################
default_UNSW = { # Default question
    'name': 'default_UNSW',
    'questions': [
        {
            'question': 'What is the fox’s name that ran amok on campus?',
            'options': [
                'Frankie',
                'Frank',
                'Megan',
                'James'
            ]
        },
        {
            'question': 'When will UNSW switch to 100% renewable energy?',
            'options': [
                '2020',
                '2030',
                '2025',
                '2035'
            ]
        },
        {
            'question': 'Who is the best COMP1531 tutor?',
            'options' : [
                'Victor Fang',
                'Victor Claw',
                'Victor Tooth',
                'Bob'
            ]
        },
        {
            'question': 'What does CSE stand for?',
            'options': [
                'Computer Science and Engineering',
                'Computer Software Engineering',
                'Coding’s So Easy',
                'Code Sciences and Engineering'
            ]
        },
        {
            'question': 'How many calories does walking up the Basser Steps burn?',
            'options': [
                '30',
                '35',
                '24',
                '20'
            ]
        }
    ]
}

# trivias = {
#     channel_id,
#     trivia_active,
#     current_category,
#     categories: [category],
#     time_limit,
#     msg_ids,
#     points,
# }

# category = {
#     name,
#     questions: [question],
# }

# question = {
#     question,
#     options: [],
#     correct_option,
# }

# points = {
#         u_id: point
# }

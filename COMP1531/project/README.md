# COMP1531 Major Project

## Changelog

* 28-10: Adding password reset as routes not automatically auth checking
* 29-10: 6.1 section updated with corrected types

## Contents

  1. Aims
  2. Overview
  3. Iteration 1: Basic functionality and tests
  4. Iteration 2: Not yet released
  5. Iteration 3: Not yet released
  6. Interface specifications
  7. Due Dates and Weightings
  8. Other Expectations
  9. Plagiarism

## 1. Aims:

* To provide students with hands on experience testing, developing, and maintaining a backend server in python.
* To develop students' problem solving skills in relation to the software development lifecycle.
* Learn to work effectively as part of a team by managing your project, planning, and allocation of responsibilities among the members of your team.
* Gain experience in collaborating through the use of a source control and other associated modern team-based tools.
* Apply appropriate design practices and methodologies in the development of their solution
* Develop an appreciation for product design and an intuition of how a typical customer will use a product.

## 2. Overview

To manage the transition from trimesters to hexamesters in 2020, UNSW has established a new focus on building an in-house digital collaboration and communication tool for groups and teams to support the high intensity learning environment.

Rather than re-invent the wheel, UNSW has decided that it finds the functionality of **<a href="https://flock.com/">Flock</a>** to be nearly exactly what it needs. For this reason, UNSW has contracted out Pineapple Pty Ltd (a small software business run by Hayden) to build the new product. In UNSW's attempt to connect with the younger and more "hip" generation that fell in love with flickr, Tumblr, etc, they would like to call the new UNSW-based product **flockr**.

Pineapple Pty Ltd has sub-contracted two software firms:

* Catdog Pty Ltd (two software developers, Sally and Bob, who will build the initial web-based GUI)
* YourTeam Pty Ltd (a team of talented misfits completing COMP1531 in 20T3), who will build the backend python server and possibly assist in the GUI later in the project

In summary, UNSW contracts Pineapple Pty Ltd, who sub contracts:

* Catdog (Sally and Bob) for front end work
* YourTeam (you and others) for backend work

Pineapple Pty Ltd met with Sally and Bob (the front end development team) 2 weeks ago to brief them on this project. While you are still trying to get up to speed on the requirements of this project, Sally and Bob understand the requirements of the project very well.

Because of this they have already specified a **common interface** for the frontend and backend to operate on. This allows both parties to go off and do their own development and testing under the assumption that both parties comply will comply with the common interface. This is the interface **you are required to use**

Besides the information available in the interface that Sally and Bob provided, you have been told (so far) that the features of flockr that UNSW would like to see implemented include:

1. Ability to login, register if not registered, and log out
2. Ability to reset password if forgotten
3. Ability to see a list of channels
4. Ability to create a channel, join a channel, invite someone else to a channel, and leave a channel
5. Within a channel, ability to view all messages, view the members of the channel, and the details of the channel
6. Within a channel, ability to send a message now, or to send a message at a specified time in the future
7. Within a channel, ability to edit, remove, pin, unpin, react, or unreact to a message
8. Ability to view user anyone's user profile, and modify a user's own profile (name, email, handle, and profile photo)
9. Ability to search for messages based on a search string
10. Ability to modify a user's admin permissions: (MEMBER, OWNER)
11. Ability to begin a "standup", which is an X minute period where users can send messages that at the end of the period will automatically be collated and summarised to all users

The specific capabilities that need to be built for this project are described in the interface at the bottom. This is clearly a lot of features, but not all of them are to be implemented at once (see below)

## 3. Iteration 1: Basic functionality and tests

Complete. Please see commit history to view old iteration info.

## 4. Iteration 2

Complete. Please see commit history to view old iteration info.

## 5. Iteration 3

Iteration 3 builds off all of the work you've completed in iteration 2.

If you haven't completed the implementations for iteration 2, you must complete them as part of this iteration. The automarks for iteration 3 will test on a fully completed interface - i.e. the work you've had to do for iteration 1, 2, 3.

### 5.1. Task

In this iteration, you are expected to:

1. Implement and test the HTTP Flask server according to the entire interface provided in the specification, including features that were added in iteration 3, including:
    * `message/sendlater`
    * `message/react`
    * `message/unreact`
    * `message/pin`
    * `message/unpin`
    * `/user/profile/uploadphoto`
    * `standup/start`
    * `standup/active`
    * `standup/send`
    * `auth/passwordreset/request`
    * `auth/passwordreset/reset`

    Part of this section may be automarked.

    Pylint is assessed identical to that of iteration 2.

    *Branch* coverage for all .py files that aren't tests is assessed identical to that of iteration 2.

    You can structure your tests however you choose, as long as they are appended with `_test.py`.

    A frontend has been built by Sally & Bob that you can use in this iteration, and use your backend to power it (note: an incomplete backend will mean the frontend cannot work). **You can, if you wish, make changes to the frontend code, but it is not required for this iteration.** As part of this iteration it's required that your backend code can correctly power the frontend.

    You must comply with instructions laid out in `4.2`

2. Continue demonstrating effective project management and effective git usage

    Part of this section may be automarked.

    You will be heavily marked for your use of thoughtful project management and use of git effectively. The degree to which your team works effectively will also be assessed.

3. Document the planning of new features.

    You are required to scope out 2-3 problems to solve for future iterations of flockr. You aren't required to build/code them, but you are required to go through SDLC steps of requirements analysis, conceptual modelling, and design.

    Full detail of this can be found in `5.3`.

### 5.2. How to implement and test features

Continue working this project by making distinct "features". Each feature should add some meaningful functionality to the project, but still be as small as possible. You should aim to size features as the smallest amount of functionality that adds value without making the project more unstable. For each feature you should:

1. Create a new branch.
2. Write tests for that feature and commit them to the branch.
3. Implement that feature.
4. Make any changes to the tests such that they pass with the given implementation. You should not have to do a lot here. If you find that you are, you're not spending enough time on step 2.
5. Create a merge request for the branch.
6. Get someone in your team who **did not** work on the feature to review the merge request. When reviewing, **not only should you ensure the new feature has tests that pass, but you should also check that the coverage percentage has not been significantly reduced.**
7. Fix any issues identified in the review.
8. Merge the merge request into master.

For this project, a feature is typically sized somewhere between a single function, and a whole file of functions (e.g. `auth.py`). It is up to you and your team to decide what each feature is.

There is no requirement that each feature be implemented by only one person. In fact, we encourage you to work together closely on features, especially to help those who may still be coming to grips with python.

Please pay careful attention to the following:

Your tests, keep in mind the following:
* We want to see **evidence that you wrote your tests before writing the implementation**. As noted above, the commits containing your initial tests should appear *before* your implementation for every feature branch. If we don't see this evidence, we will assume you did not write your tests first and your mark will be reduced.
* You should have black-box tests for all tests required (i.e. testing each function/endpoint). However, you are also welcome to write whitebox unit tests in this iteration if you see that as important.
* Merging in merge requests with failing pipelines is **very bad practice**. Not only does this interfere with your teams ability to work on different features at the same time, and thus slow down development, it is something you will be penalised for in marking.
* Similarly, merging in branches with untested features is also **very bad practice**. We will assume, and you should too, that any code without tests does not work.
* Pushing directly to `master` is not possible for this repo. The only way to get code into master is via a merge request. If you discover you have a bug in `master` that got through testing, create a bugfix branch and merge that in via a merge request.

### 5.3. Planning for the next problems to solve

Software development is an iterative process - we're never truly finished. As we complete the development and testing of one feature, we're often then trying to understand the requirements and needs of our users to design the next set of features in our product.

For iteration 3 you are going to produce a short report in `planning.pdf` and place it in the repository. The contents of this report will be a simplified approach to understanding user problems, developing requirements, and doing some early designs.

N.B. If you don't know how to produce a PDF, you can easily make one in google docs and then export to PDF.

#### [Requirements] Elicitation

Find 2-3 people to interview as target users. Target users are people who currently use a tool like flockr, or intend to. Collect their name and email address.

Develop a series of questions to ask these target users to understand what *problems* they might have with teamwork-driven communication tools that are currently unsolved by flockr. Give these questions to your target users and record their answers. 

#### [Requirements] Analysis & Specification - Use Cases

Once you've elicited this information, it's time to consolidate it.

Take the responses from the elicitation and express these requirements as **User Stories**. Document these user stories. For each user story, add User Acceptance Criteria as notes so that you have a clear definition of when a story has been completed.

Once documented, generate at least one use case that attempts to tell a story of a solution that satifies the requirements elicited. You can generate a visual diagram or a more written-recipe style, as per lectures.

#### [Requirements] Validation

With your completed use case work, reach out to the 2-3 people you interviewed originally and inquire as to the extent to which these use cases would adequately describe the problem they're trying to solve. Ask them for a comment on this, and record their comments in the PDF.

#### [Design] Interface Design

Now that we've established our _problem_ (described as requirements), it's time to think about our _solution_ in terms of what capabilities would be necessary. You will specify these capabilities as HTTP endpoints, similar to what is described in `6.2`. There is no minimum or maximum of what is needed - it will depend on what problem you're solving.

#### [Design] Conceptual Modelling (State)

Now that you have a sense of the problem to solve, and what capabilities you will need to provide to solve it, add at least one state diagram to your PDF to show how the state of the application would change based on user actions. The aim of this diagram is how to a developer understand the different states the user or application.

### 5.4. Marking Criteria

|Section|Weighting|Criteria|
|---|---|---|
|Testing|25%|<ul><li>Tests provide excellent test **coverage** with the coverage tool</li><li>Demonstrated an understanding of the importance of **clarity** on the communication of test purposes</li><li>Demonstrated an understanding of thoughtful test **design**</li><li>Performance against an automatic marking syste<m/li><li>Compliance with standard pylint requirements</li></ul>|
|Implementation|25%|<ul><li>Correctly implemented entire backend server interface that satisfies requirements</li><li>Pythonic programming approach (where possible)</li><li>Thought out code design inline with principles discussed in lectures</li><li>Compliance with standard pylint requirements</li></ul>|
|Next Stage: Requirements & Design|20%|<ul><li>Requirements elicited from potential users, recorded as user stories</li><li>User journey justified and expressed as use case(s)</li><li>Interface proposed as a potential solution to provide capabilities</li><li>State diagram drawn to demonstrate how application responds to actions</li></ul>|
|Git practices & Project Management|20%|<ul><li>Meaningful and informative git commit names being used</li><li>Effective use of merge requests (from branches being made) across the team</li><li>Effective use of course-provided flockr, demonstrating an ability to communicate and manage effectivelly digitally</li><li>Use of task board on Gitlab to track and manage tasks</li><li>Effective use of agile methods such as standups</li></ul>|
|Teamwork|10%|<ul><li>A generally equal contribution between team members</li><li>Clear evidence of reflection on group's performance and state of the team, with initiative to improve in future iterations</li></ul>|
|(Bonus Marks) Extra Features|20%|<ul><li>Up to 20% extra marks can be gained through additions of "extra feature(s)".</li><li>Marks will be awarded based on 1) Originality, 2) Technical or creative achievement, 3) Lack of bugs associated with it, 4) Size/scale of the addition.</li><li>Your tutor is not required to provide any assistance with this, as it's intended for more advanced students once they complete all other criteria at a high level of quality.</li><li>A brief explanation of your additions must be written in a file `extra.md` that is added to your repo.</li><li>Section 5.8 provides some examples of extra features you may want to implement, if you need some suggestions.</li>|

For this and for all future milestones, you should consider the other expectations as outlined in section 8 below.

### 5.5. Storing data

You are not required to store data persistently in this iteration. However, you are welcome to implement basic persistence if you find it convenient.

### 5.6. Submission

This iteration is due to be submitted at 8pm Sunday 15th November (**week 9**). You will then be demonstrating this in your week 10 lab. All team members **must** attend this lab session, or they will not receive a mark.

At the due date provided, we will automatically collect and submit the code that is on the `master` branch of your repository. If the deadline is approaching and you have features that are either untested or failing their tests, **DO NOT MERGE IN THOSE MERGE REQUESTS**. Your tutor will look at unmerged branches and may allocate some reduced marks for incomplete functionality, but `master` should only contain working code.

### 5.7. Demonstration

When you demonstrate this iteration in your week 10 lab, it will consist of a 15 minute Q&A in front of your tutorial class via zoom. Webcams are required to be on during this Q&A (your phone is a good alternative if your laptop/desktop doesn't have a webcam).

### 5.8. Extra Features Suggestions

#### Frontend
​
**Hangman on Frontend**
​
After a game of Hangman has been started any user in the channel can type /guess X where X is an individual letter. If that letter is contained in the word or phrase they're trying to guess, the app should indicate where it occurs. If it does not occur, more of the hangman is drawn. There is a lot of flexibility in how you achieve this. It can be done only by modifying the backend and relying on messages to communicate the state of the game (e.g. after making a guess, the "Hangman" posts a message with a drawing of the hangman in ASCII/emoji art). Alternatively you can modify the frontend, if you want to experiment with fancier graphics.

The app should use words and phrases from an external source, not just a small handful hardcoded into the app. One suitable source is /usr/share/dict/words available on Unix-based systems. Alternatively, the python wikiquote module is available via pip and can be used to retrieve quotes and phrases from Wikiquote.

Note that this part of the specification is deliberately open-ended. You're free to make your own creative choices in exactly how the game should work, as long as the end result is something that could be fairly described as Hangman.
​
**admin/user/remove full implementation (frontend and backend)**
​
`admin/user/remove       DELETE      (token, u_id)           {}`
​
InputError when:u_id does not refer to a valid user
AccessError whenThe authorised user is not an owner of the slackr
​
Given a User by their user ID, remove the user from the slackr.
​
#### Databases
​
Implementing persistence using a form of database. Ways to do this in python include:
    * Using the `sqlite3` or `peewee` or `psycopg2` modules to run SQL queries on a local .db file, for people studying/have studied COMP3311 may find this integrates well
    * Using the `sqlite3` or `peewee` or `psycopg2` to run SQL queries on a local .db file OR a remote database (using Postgresql or MySQL)
​
#### Object-Oriented Programming
​
Refactor your code so it is stored in objects instead of dictionaries (if it's not already) and make use of OO concepts taught in lectures to pass data around the backend.
​
#### Deployment
​
Deploying your project using heroku or something similar (not sure if this is possible/allowed)

## 6. Interface specifications

These interface specifications come from Sally and Bob, who are building the frontend to the requirements set out below.

### 6.1. Data types

|Variable name|Type|
|-------------|----|
|named exactly **email**|string|
|named exactly **id**|integer|
|named exactly **length**|integer|
|named exactly **password**|string|
|named exactly **token**|string|
|named exactly **message**|string|
|contains substring **name**|string|
|contains substring **code**|string|
|has prefix **is_**|boolean|
|has prefix **time_**|integer (unix timestamp), [check this out](https://www.tutorialspoint.com/How-to-convert-Python-date-to-Unix-timestamp)|
|has suffix **_id**|integer|
|has suffix **_url**|string|
|has suffix **_str**|string|
|has suffix **end**|integer|
|has suffix **start**|integer|
|(outputs only) named exactly **user**|Dictionary containing u_id, email, name_first, name_last, handle_str, profile_img_url|
|(outputs only) named exactly **users**|List of dictionaries, where each dictionary contains types u_id, email, name_first, name_last, handle_str, profile_img_url|
|(outputs only) named exactly **messages**|List of dictionaries, where each dictionary contains types { message_id, u_id, message, time_created, reacts, is_pinned  }|
|(outputs only) named exactly **channels**|List of dictionaries, where each dictionary contains types { channel_id, name }|
|(outputs only) name ends in **members**|List of dictionaries, where each dictionary contains types { u_id, name_first, name_last, profile_img_url }|
|(outputs only) name ends in **reacts**|List of dictionaries, where each dictionary contains types { react_id, u_ids, is_this_user_reacted } where react_id is the id of a react, and u_ids is a list of user id's of people who've reacted for that react. is_this_user_reacted is whether or not the authorised user has been one of the reacts to this post|



### 6.2. Interface

|Function Name|HTTP Method|Parameters|Return type|Exceptions|Description|
|------------|-------------|----------|-----------|----------|----------|
|auth/login|POST|(email, password)|{ u_id, token }|**InputError** when any of:<ul><li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method)</li><li>Email entered does not belong to a user</li><li>Password is not correct</li></ul> | Given a registered users' email and password and generates a valid token for the user to remain authenticated |
|auth/logout|POST|(token)|{ is_success }|N/A|Given an active token, invalidates the token to log the user out. If a valid token is given, and the user is successfully logged out, it returns true, otherwise false. |
|auth/register|POST|(email, password, name_first, name_last)|{ u_id, token }|**InputError** when any of:<ul><li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method).</li><li>Email address is already being used by another user</li><li>Password entered is less than 6 characters long</li><li>name_first not is between 1 and 50 characters inclusively in length</li><li>name_last is not between 1 and 50 characters inclusively in length</ul>|Given a user's first and last name, email address, and password, create a new account for them and return a new token for authentication in their session. A handle is generated that is the concatentation of a lowercase-only first name and last name. If the concatenation is longer than 20 characters, it is cutoff at 20 characters. If the handle is already taken, you may modify the handle in any way you see fit (maintaining the 20 character limit) to make it unique. |
|auth/passwordreset/request|POST|(email)|{}|N/A|Given an email address, if the user is a registered user, send's them a an email containing a specific secret code, that when entered in auth_passwordreset_reset, shows that the user trying to reset the password is the one who got sent this email.|
|auth/passwordreset/reset|POST|(reset_code, new_password)|{}|**InputError** when any of:<ul><li>reset_code is not a valid reset code</li><li>Password entered is not a valid password</li>|Given a reset code for a user, set that user's new password to the password provided|
|channel/invite|POST|(token, channel_id, u_id)|{}|**InputError** when any of:<ul><li>channel_id does not refer to a valid channel.</li><li>u_id does not refer to a valid user</li></ul>**AccessError** when<ul><li>the authorised user is not already a member of the channel</li>|Invites a user (with user id u_id) to join a channel with ID channel_id. Once invited the user is added to the channel immediately|
|channel/details|GET|(token, channel_id)|{ name, owner_members, all_members }|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li></ul>**AccessError** when<ul><li>Authorised user is not a member of channel with channel_id</li></ul>|Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel|
|channel/messages|GET|(token, channel_id, start)|{ messages, start, end }|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>start is greater than the total number of messages in the channel</li></ul>**AccessError** when<ul><li>Authorised user is not a member of channel with channel_id</li></ul>|Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.|
|channel/leave|POST|(token, channel_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li></ul>**AccessError** when<ul><li>Authorised user is not a member of channel with channel_id</li></ul>|Given a channel ID, the user removed as a member of this channel|
|channel/join|POST|(token, channel_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li></ul>**AccessError** when<ul><li>channel_id refers to a channel that is private (when the authorised user is not a global owner)</li></ul>|Given a channel_id of a channel that the authorised user can join, adds them to that channel|
|channel/addowner|POST|(token, channel_id, u_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>When user with user id u_id is already an owner of the channel</li></ul>**AccessError** when the authorised user is not an owner of the flockr, or an owner of this channel</li></ul>|Make user with user id u_id an owner of this channel|
|channel/removeowner|POST|(token, channel_id, u_id)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>When user with user id u_id is not an owner of the channel</li></ul>**AccessError** when the authorised user is not an owner of the flockr, or an owner of this channel</li></ul>|Remove user with user id u_id an owner of this channel|
|channels/list|GET|(token)|{ channels }|N/A|Provide a list of all channels (and their associated details) that the authorised user is part of|
|channels/listall|GET|(token)|{ channels }|N/A|Provide a list of all channels (and their associated details)|
|channels/create|POST|(token, name, is_public)|{ channel_id }|**InputError** when any of:<ul><li>Name is more than 20 characters long</li></ul>|Creates a new channel with that name that is either a public or private channel|
|message/send|POST|(token, channel_id, message)|{ message_id }|**InputError** when any of:<ul><li>Message is more than 1000 characters</li></ul>**AccessError** when: <li> the authorised user has not joined the channel they are trying to post to</li></ul>|Send a message from authorised_user to the channel specified by channel_id|
|message/remove|DELETE|(token, message_id)|{}|**InputError** when any of:<ul><li>Message (based on ID) no longer exists</li></ul>**AccessError** when none of the following are true:<ul><li>Message with message_id was sent by the authorised user making this request</li><li>The authorised user is an owner of this channel or the flockr</li></ul>|Given a message_id for a message, this message is removed from the channel|
|message/edit|PUT|(token, message_id, message)|{}|**AccessError** when none of the following are true:<ul><li>Message with message_id was sent by the authorised user making this request</li><li>The authorised user is an owner of this channel or the flockr</li></ul>|Given a message, update it's text with new text. If the new message is an empty string, the message is deleted.|
|message/sendlater|POST|(token, channel_id, message, time_sent)|{ message_id }|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>Message is more than 1000 characters</li><li>Time sent is a time in the past</li></ul>**AccessError** when: <li> the authorised user has not joined the channel they are trying to post to</li></ul>|Send a message from authorised_user to the channel specified by channel_id automatically at a specified time in the future|
|message/react|POST|(token, message_id, react_id)|{}|**InputError** when any of:<ul><li>message_id is not a valid message within a channel that the authorised user has joined</li><li>react_id is not a valid React ID. The only valid react ID the frontend has is 1</li><li>Message with ID message_id already contains an active React with ID react_id from the authorised user</li></ul>|Given a message within a channel the authorised user is part of, add a "react" to that particular message|
|message/unreact|POST|(token, message_id, react_id)|{}|**InputError**   <ul><li>message_id is not a valid message within a channel that the authorised user has joined</li><li>react_id is not a valid React ID</li><li>Message with ID message_id does not contain an active React with ID react_id</li></ul>|Given a message within a channel the authorised user is part of, remove a "react" to that particular message|
|message/pin|POST|(token, message_id)|{}|**InputError** when any of:<ul><li>message_id is not a valid message</li><li>Message with ID message_id is already pinned</li></ul>**AccessError** when any of:<ul><li>The authorised user is not a member of the channel that the message is within</li><li>The authorised user is not an owner</li></ul>|Given a message within a channel, mark it as "pinned" to be given special display treatment by the frontend|
|message/unpin|POST|(token, message_id)|{}|**InputError** when any of:<ul><li>message_id is not a valid message</li><li>Message with ID message_id is already unpinned</li></ul>**AccessError** when any of:<ul><li>The authorised user is not a member of the channel that the message is within</li><li>The authorised user is not an owner</li></ul>|Given a message within a channel, remove it's mark as unpinned|
|user/profile|GET|(token, u_id)|{ user }|**InputError** when any of:<ul><li>User with u_id is not a valid user</li></ul>|For a valid user, returns information about their user_id, email, first name, last name, and handle|
|user/profile/setname|PUT|(token, name_first, name_last)|{}|**InputError** when any of:<ul><li>name_first is not between 1 and 50 characters inclusively in length</li><li>name_last is not between 1 and 50 characters inclusively in length</ul></ul>|Update the authorised user's first and last name|
|user/profile/setemail|PUT|(token, email)|{}|**InputError** when any of:<ul><li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method).</li><li>Email address is already being used by another user</li>|Update the authorised user's email address|
|user/profile/sethandle|PUT|(token, handle_str)|{}|**InputError** when any of:<ul><li>handle_str must be between 3 and 20 characters</li><li>handle is already used by another user</li></ul>|Update the authorised user's handle (i.e. display name)|
|/user/profile/uploadphoto|POST|(token, img_url, x_start, y_start, x_end, y_end)|{}|**InputError** when any of:<ul><li>img_url returns an HTTP status other than 200.</li><li>any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL.</li><li>Image uploaded is not a JPG</li></ul>|Given a URL of an image on the internet, crops the image within bounds (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.|
|users/all|GET|(token)|{ users}|N/A|Returns a list of all users and their associated details|
|admin/userpermission/change|POST|(token, u_id, permission_id)|{}|**InputError** when any of:<ul><li>u_id does not refer to a valid user<li>permission_id does not refer to a value permission</li></ul>**AccessError** when<ul><li>The authorised user is not an owner</li></ul>|Given a User by their user ID, set their permissions to new permissions described by permission_id|Given a User by their user ID, set their permissions to new permissions described by permission_id|
|search|GET|(token, query_str)|{ messages }|N/A|Given a query string, return a collection of messages in all of the channels that the user has joined that match the query|
|clear|DELETE|()|{}|N/A|Resets the internal data of the application to it's initial state|
|standup/start|POST|(token, channel_id, length)|{ time_finish }|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>An active standup is currently running in this channel</li></ul>|For a given channel, start the standup period whereby for the next "length" seconds if someone calls "standup_send" with a message, it is buffered during the X second window then at the end of the X second window a message will be added to the message queue in the channel from the user who started the standup. X is an integer that denotes the number of seconds that the standup occurs for|
|standup/active|GET|(token, channel_id)|{ is_active, time_finish }|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li></ul>|For a given channel, return whether a standup is active in it, and what time the standup finishes. If no standup is active, then time_finish returns None|
|standup/send|POST|(token, channel_id, message)|{}|**InputError** when any of:<ul><li>Channel ID is not a valid channel</li><li>Message is more than 1000 characters</li><li>An active standup is not currently running in this channel</li></ul>**AccessError** when<ul><li>The authorised user is not a member of the channel that the message is within</li></ul>|Sending a message to get buffered in the standup queue, assuming a standup is currently active|

### 6.3. Errors for all functions

Either an `InputError` or `AccessError` is thrown when something goes wrong. All of these cases are listed in the **Interface** table.

One exception is that, even though it's not listed in the table, for all functions except `auth/register`, `auth/login`, `auth/passwordreset/request` and `auth/passwordreset/reset`, an `AccessError` is thrown when the token passed in is not a valid token.

### 6.4. Token

Many of these functions (nearly all of them) need to be called from the perspective of a user who is logged in already. When calling these "authorised" functions, we need to know:
1) Which user is calling it
2) That the person who claims they are that user, is actually that user

We could solve this trivially by storing the user ID of the logged in user on the front end, and every time the front end (from Sally and Bob) calls your background, they just sent a user ID. This solves our first problem (1), but doesn't solve our second problem! Because someone could just "hack" the front end and change their user id and then log themselves in as someone else.

To solve this when a user logs in or registers the backend should return a "token" (an authorisation hash) that the front end will store and pass into most of your functions in future. When these "authorised" functions are called, those tokens returned from register/login will be passed into those functions, and from there you can check if a token is valid, and determine the user ID.

Passwords must be stored in an encrypted form, and tokens must use JWTs (or similar).

### 6.5. Pagination

The behaviour in which channel_messages returns data is called **pagination**. It's a commonly used method when it comes to getting theoretially unbounded amounts of data from a server to display on a page in chunks. M0ost of the timelines you know and love - Facebook, Instagram, LinkedIn - do this.

For example, if we imagine a user with token "12345" is trying to read messages from channel with ID 6, and this channel has 124 messages in it, 3 calls from the client to the server would be made. These calls, and their corresponding return values would be:
 * channel_messages("12345", 6, 0) => { [messages], 0, 50 }
 * channel_messages("12345", 6, 50) => { [messages], 50, 100 }
 * channel_messages("12345", 6, 100) => { [messages], 100, -1 }

### 6.6. Permissions:
 * Members in a channel have one of two channel permissions.
   1) Owner of the channel (the person who created it, and whoever else that creator adds)
   2) Members of the channel
 * Flockr users have two global permissions
   1) Owners (permission id 1), who can also modify other owners' permissions.
   2) Members (permission id 2), who do not have any special permissions
* All flockr users are members by default, except for the very first user who signs up, who is an owner

A user's primary permissions are their global permissions. Then the channel permissions are layered on top. For example:
* An owner of flockr has owner permissions in every channel they've joined
* A member of flockr is a member in channels they are not owners of
* A member of flockr is an owner in channels they are owners of

### 6.7. Working with the frontend

There is a SINGLE repository available for all students at https://gitlab.cse.unsw.edu.au/COMP1531/20T3/project-frontend. You can clone this frontend locally. The course notice said you will receive your own copy of this, however, that isn't necessary anymore since most groups will not modify the frontend repo. If you'd like to modify the frontend repo (i.e. teach yourself some frontend), please FORK the repository.

If you run the frontend at the same time as your flask server is running on the backend, then you can power the frontend via your backend.

#### 6.7.1.

A working example of the frontend can be used at http://flockr-unsw.herokuapp.com/

The data is reset daily, but you can use this link to play around and get a feel for how the application should behave.

#### 6.7.2. Error raising for the frontend

For errors to be appropriately raised on the frontend, they must be raised by the following:

```python
if True: # condition here
    raise InputError(description='Description of problem')
```

The descriptions will not be assessed, they are just there for the frontend to help users.

The types in error.py have been modified appropriately for you.

### 6.8. Reacts

The only React ID currently associated with the frontend is React ID 1, which is a thumbs up. You are welcome to add more (this will require some frontend work)

### 6.9. Standups

Once standups are finished, all of the messages sent to standup/send are packaged together in *one single message* posted by *the user who started the standup* and sent as a message to the channel the standup was started in, timestamped at the moment the standup finished.

The structure of the packaged message is like this:

[message_sender1_handle]: [message1]

[message_sender2_handle]: [message2]

[message_sender3_handle]: [message3]

[message_sender4_handle]: [message4]

For example:

```txt
hayden: I ate a catfish
rob: I went to kmart
michelle: I ate a toaster
isaac: my catfish ate a toaster
```

Standups can be started on the frontend by typing "/standup X", where X is the number of seconds that the standup lasts for, into the message input and clicking send.

### 6.10. profile_img_url & image uploads

For outputs with data pertaining to a user, a profile_img_url is present. When images are uploaded for a user profile, after processing them you should store them on the server such that your server now locally has a copy of the cropped image of the original file linked. Then, the profile_img_url should be a URL to the server, such as http://localhost:5001/imgurl/adfnajnerkn23k4234.jpg (a unique url you generate).

Note: This is most likely the most challenging part of the project. Don't get lost in this, we would strongly recommend most teams complete this capability *last*.

### 6.11. Other Points

* Each message should have it's own unique ID. I.E. No messages should share an ID with another message, even if that other message is in a different channel.

## 7. Due Dates and Weightings

|Iteration|Code and report due                  |Demonstration to tutor(s)      |Assessment weighting of project (%)|
|---------|-------------------------------------|-------------------------------|-----------------------------------|
|   1     |8pm Sunday 4th October (**week 3**)   |In YOUR **week 4** laboratory  |30%                                |
|   2     |8pm Monday 26th October (**week 7**)   |In YOUR **week 7** laboratory  |40%                                |
|   3     |8pm Sunday 15th November (**week 9**)   |In YOUR **week 10** laboratory |30%                                |

There is no late penalty, as we do not accept late submissions.

## 8. Other Expectations

While it is up to you as a team to decide how work is distributed between you, for the purpose of assessment there are certain key criteria all members must.

* Code contribution
* Documentation contribution
* Usage of git/GitLab
* Attendance
* Peer assessment
* Academic conduct

The details of each of these is below.

While, in general, all team members will receive the same mark (a sum of the marks for each iteration), **if you as an individual fail to meet these criteria your final project mark may be scaled down**, most likely quite significantly.

### 8.1. Progress check-in

During your lab class, in weeks without demonstrations (see below), you and your team will conduct a short stand-up in the presence of your tutor. Each member of the team will briefly state what they have done in the past week, what they intend to do over the next week, and what issues they faced or are currently facing. This is so your tutor, who is acting as a representative of the client, is kept informed of your progress. They will make note of your presence and may ask you to elaborate on the work you've done.

### 8.2. Code contribution

All team members must contribute code to the project. Tutors will assess the degree to which you have contributed by looking at your **git history** and analysing lines of code, number of commits, timing of commits, etc. If you contribute significantly less code than your team members, your work will be closely examined to determine what scaling needs to be applied.

### 8.3. Documentation contribution

All team members must contribute documentation to the project. Tutors will assess the degree to which you have contributed by looking at your **git history** but also **asking questions** (essentially interviewing you) during your demonstration.

Note that, **contributing more documentation is not a substitute for not contributing code**.

### 8.4. Peer Assessment

You will be required to complete a form in week 10 where you rate each team member's contribution to the project and leave any comments you have about them. Information on how you can access this form will be released closer to Week 10. Your other team members will **not** be able to see how you rated them or what comments you left.

If your team members give you a less than satisfactory rating, your contribution will be scrutinised and you may find your final mark scaled down.

### 8.5. Attendance

It is generally assumed that all team members will be present at the demonstrations and at weekly check-ins. If you're absent for more than 80% of the weekly check-ins or any of the demonstrations, your mark may be scaled down.

If, due to exceptional circumstances, you are unable to attend your lab for a demonstration, inform your tutor as soon as you can so they can record your absence as planned.

## 9. Plagiarism

The work you and your group submit must be your own work. Submission of work partially or completely derived from any other person or jointly written with any other person is not permitted. The penalties for such an offence may include negative marks, automatic failure of the course and possibly other academic discipline. Assignment submissions will be examined both automatically and manually for such submissions.

Relevant scholarship authorities will be informed if students holding scholarships are involved in an incident of plagiarism or other misconduct.

Do not provide or show your project work to any other person, except for your group and the teaching staff of COMP1531. If you knowingly provide or show your assignment work to another person for any reason, and work derived from it is submitted you may be penalized, even if the work was submitted without your knowledge or consent. This may apply even if your work is submitted by a third party unknown to you.

Note, you will not be penalized if your work has the potential to be taken without your consent or knowledge.

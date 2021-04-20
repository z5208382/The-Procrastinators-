# TRIVIA Explanations


## All trivia commands
|Function name|HTTP method|Parameters|Return type|Exceptions|Descriptions|
|-------------|-----------|----------|-----------|----------|------------|
|trivia_check_command|POST|token, channel_id, message|{'message'}|InputError:<ul><li>Message does not match any commands</li></ul>|If ‘/trivia’ is typed in, message send calls this function to check which command was entered. This function will then call relevant functions based on the command entered: <ul><li>`/trivia` (shows instructions)</li><li>`/trivia create <name of new category>`</li><li>`/trivia add_questions <name of category>`<li>`/trivia start <name of category>`<li>`/trivia end`<li>`/trivia time`</ul>|
|trivia_instructions|POST|channel_id|{'message'}|None|If only `/trivia` is typed in, this function is called, which sends a message with a list of the available categories and the possible commands|
|trivia_create|POST|token, channel_id|{'message'}|InputError:<ul><li>Name exceeds 50 characters</li><li>Name already exists</li>|Creates a new trivia category. Returns success message - "\<name> category has been successfully created; to enter questions type ..."|
|trivia_addquestions|POST|token, channel_id, category_name, message|{'message'}|InputError:<ul><li>options provided less than 2</li><li>Category name does not exist</li>|Allows user to add questions to a category. User inputs question and options between 2 to 4 only and the options are each followed by a new line <br>Display Error message:<br>Please enter options with the question (and will show how to format entering the question + options)|
|trivia_start|POST|token, channel_id, category_name|{'message'}|InputError:<ul><li>Trivia has already started</li><li>The given category does not exist</li><li>The given category has no questions</li>|The questions and options in the category will be sent as individual messages to the channel. To choose an option, each user must react to the message. At the end of the specified time limit, the reacts are checked. After the time limit is over, reacts made for any answer will not be counted in final points for the user. Each question is worth 1 point. When all questions have been displayed, trivia_end is called.|
|trivia_end|POST|token,channel_id, category_name|{'message'}|InputError:<ul><li>No trivia currently active</li><ul>|Allows users to end a currently running trivia. Displays scoreboard of users participating.|
|trivia_time|POST|token, channel_id, time_limit|{'message'}|InputError:<ul><li>time_limit not a multiple of 5 seconds</li><li>time_limit not between 5 and 20 seconds</li>|Allow users to choose how much time is given for each question. Can be intervals of 5 seconds, and only between 5 and 20 seconds. The default is 10 seconds.|

## Extra features
* Anti-cheat feature:<br>
    Users reacting to more than one options will be punished by zero-ing their scores

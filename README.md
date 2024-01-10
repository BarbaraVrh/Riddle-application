# Riddle_application
This is a riddle application consisting of 4 questions. It is developed using python and flask framework.
It contains 3 html templates : index, get_riddle and end. They are used to input user's name, fetch a riddle and display the end page respectively.
As for the riddle game python file, it first saves user's name in the sql database, after which it retrieves the riddles from the database. After that the app uses a combination of get and post requests to provide a question for the user, record their answer and then checks whether it is correct before the user can move on to the next question. After the user answers all the questions, the riddle game is done.
Additionally, a sql connector file is needed which will depend on the server and database used.

This project was created for a software engineering class with Sam Solheim and Morgan Bergstorm.

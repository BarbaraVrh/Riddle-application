import secrets
from flask import Flask, render_template, request, redirect, url_for,session
import random
import collections
collections.MutableSequence = collections.abc.MutableSequence
collections.Iterable = collections.abc.Iterable
from flask_navigation import Navigation
# Import needed connection information from azuresqlconnector
from azuresqlconnector import *



app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

# Following Line sets up the session (hosted on client side)
# Note: We don't really have sensitive data for this, so not a big concern security-wise. 
app.config.from_mapping(SECRET_KEY = secrets.token_hex(16))


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/submit_name', methods = ["POST"])
def name_submit():
    riddles=get_riddles()
    UserName = request.form["User_Name"]
    session["user_name"] = UserName
    
    # Initialize SQL Connection
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = f"""
    EXEC FinTest.AddChallenger @Name = '{UserName}';
    """

    cursor.execute(sql_query)
    print("Data submitted...")
    # Don't forget to commit the changes. 
    conn.commit()
    print("Changes committed.")
    cursor.close()
    session["riddles"]=riddles
    print(riddles)
        
    riddle_1 = riddles[0]
    session["riddle_1"]=riddle_1
    riddle_2 = riddles[1]
    session["riddle_2"]=riddle_2
    riddle_3= riddles[2]
    session["riddle_3"]=riddle_3
    riddle_4= riddles[3]
    session["riddle_4"]=riddle_4

    
    question_1 = riddle_1["Riddle 1"]
    session["question_1"] = question_1
    question_2 = riddle_2["Riddle 2"]
    session["question_2"] = question_2
    question_3 = riddle_3["Riddle 3"]
    session["question_3"] = question_3
    question_4 = riddle_4["Riddle 4"]
    session["question_4"]= question_4
    # Can't close the connection until the player hits game over screen. Otherwise will give error that DB connection is closed. 
    # Should be able to close our cursor and make a new one in the next section though 

    return render_template('index.html', 
                           user_name=UserName)


def get_riddles():
#### Getting riddles and answers from the database ####
    # This will be for collecting the (distinct) index numbers for the riddles. 
    riddle_index = []
    # This will be where we collect the riddles that someone will encounter in their session. 
    # Also adding a placeholder for the riddle answers
    riddles = []

    # Initialize SQL Connection
    conn2 = SQLConnection()
    conn2 = conn2.getConnection()
    riddle_cursor = conn2.cursor()

    # num_riddles will be where we store how many riddles (total) there are in the database
    total_riddles = 0
    # Query to get the number of riddles
    query_1 = f"""
    SELECT COUNT(*) FROM FinTest.SphinxRiddles;
    """
    # Calling the database to get the count from the database
    riddle_cursor.execute(query_1)
    total_riddles = riddle_cursor.fetchone()[0]
    temp_riddle_idx = list(range(1, (total_riddles+1), 1))

    # Using random.sample to get 4 index numbers of riddles
    riddle_index = random.sample(temp_riddle_idx, 4)

    query_2 = f"""
    SELECT Riddle FROM [FinProd].[SphinxRiddles] WHERE RiddleId IN (?, ?, ?, ?);
    """
    riddle_cursor.execute(query_2, tuple(riddle_index))

    # Loop 1: This loop gets the riddle text and adds them to separate dictionaries named Riddle 1, Riddle 2, ...
    for idx in range(4):
        # Need to set up temporary variables that can be reset in each iteration of the loop
        temp = {}
        temp["Riddle " + str(idx + 1)] = riddle_cursor.fetchone()[0]
        riddles.append(temp)

    query_3 = f"""
    SELECT AnswerText FROM [FinProd].[SphinxAnswers] WHERE RiddleId IN (?, ?, ?, ?);
    """
    riddle_cursor.execute(query_3, tuple(riddle_index))

    # Loop 2: This loop goes through selected riddle answers, adds them all to a list, and then brings that list into the nested dictionaries
    for idx in range(4):
        temp_ans = []
        records = riddle_cursor.fetchmany(3)
        for row in records:
            temp_ans.append(row[0])
        riddles[idx]["answers"] = temp_ans

    query_4 = f"""
    SELECT AnswerText FROM [FinProd].[SphinxAnswers] WHERE RiddleId IN (?, ?, ?, ?) AND IsCorrect = 1;
    """
    riddle_cursor.execute(query_4, tuple(riddle_index))

    # Loop 3: Finally got to this point; this loop should be easier now that everything else was figured out. Just gets the correct answer
    for idx in range(4):
        riddles[idx]["correct answer"] = riddle_cursor.fetchone()[0]
    

    # Close the cursor and connection
    riddle_cursor.close()
    
    return riddles
    


@app.route('/question', methods = ["GET","POST"])
def get_question():
    if "count" not in session:
          session["count"]=0
    if session["count"] == 4:
        return redirect(url_for('print_end'))
   

    print("the current count is", session["count"])
    

    if request.method=="GET":
        if session["count"]==0:
            riddle=session.get("riddle_1")
            question=session.get("question_1")    
        elif session.get("count")==1:
            riddle= session.get("riddle_2")
            print("the riddle 2 is", riddle)
            question=session.get("question_2")
            print("the question 2 is", question)
        elif session.get("count")==2:
            riddle= session.get("riddle_3")
            print("the riddle is", riddle)
            question=session.get("question_3")
        elif session.get("count")==3:
            riddle= session.get("riddle_4")
            question=session.get("question_4")
            print("the riddle 4 is", riddle)


        session["riddle"]=riddle
        session["question"]=question
        default_answer=riddle["answers"][0]
        print(default_answer)
        return render_template('get_riddle.html',
                        riddle=riddle,
                        count=session["count"],
                        question = question,
                        default_answer=default_answer)

    
    
    
    if request.method=="POST":
        if session.get("count")==0:
            riddle=session.get("riddle_1")
            question=session.get("question_1") 
        elif session.get("count")==1:
            riddle= session.get("riddle_2")
            print("the riddle 2 is", riddle)
            question=session.get("question_2")
            print("the question 2 is", question)
        elif session.get("count")==2:
            riddle= session.get("riddle_3")
            print("the riddle is", riddle)
            question=session.get("question_3")
        elif session.get("count")==3:
            riddle= session.get("riddle_4")
            question=session.get("question_4")
            print("the riddle 4 is", riddle)

        session["riddle"]=riddle
        session["question"]=question
        default_answer=riddle["answers"][0]
        print(default_answer)


        selected_answer=request.form["answer"]
        print("the selected answer is", selected_answer)
        correct_answer=riddle["correct answer"]
        print("the correct answer is", correct_answer)
        if selected_answer == correct_answer:
            feedback = "Congratulations! You got the answer right!"
        else:
            feedback = "Sorry, that's not the right answer. Try again!"
            return render_template(
                "get_riddle.html",
                riddle=riddle,
                answer=selected_answer,
                correct_answer=correct_answer,
                feedback=feedback,
                count=session["count"],
                question=question
                
            )
    session["count"]+=1

    
        
    return render_template(
        "get_riddle.html",
        riddle=riddle,
        answer=selected_answer,
        correct_answer=correct_answer,
        feedback=feedback,
        count=session["count"]-1,
        question=question
       
    )
 





@app.route('/end', methods=["GET"])
def print_end():
    return render_template("end.html")



if __name__ == "__main__":
    app.run(debug=True)

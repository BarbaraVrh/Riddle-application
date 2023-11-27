import secrets
from flask import Flask, render_template, request, redirect, url_for,session
import random
import collections
collections.MutableSequence = collections.abc.MutableSequence
collections.Iterable = collections.abc.Iterable
from flask_navigation import Navigation

app = Flask(__name__)

app.secret_key = 'yoursecretkey'

riddles = [
    {
        "question": "What has to be broken before you can use it?",
        "answers": ["An egg", "A promise", "A heart"],
        "correct_answer": "An egg",
    },
    {
        "question": "I am always coming, but never arrive. What am I?",
        "answers": ["A giggling map leading to the chocolate river of dreams", "Tomorrow", "Change"],
        "correct_answer": "Tomorrow",
    },
    {
        "question": "What has no beginning, end, or middle?",
        "answers": ["A donut", "A circle", "Whispering tacos on a unicycle"],
        "correct_answer": "A donut",
    },
    {
        "question": "I have no voice, but I can still speak to you. What am I?",
        "answers": ["A book", "A nightlight", "Moonwalking flamingos in a cheese factory"],
        "correct_answer": "A book",
    },
    {
        "question": "What gets wetter the more it dries?",
        "answers": ["A towel", "Fizzing kittens surfing on rainbow bubbles", "A piece of clay"],
        "correct_answer": "A towel",
    },
    {
        "question": "I fly without wings. I cry without eyes. Wherever I go, darkness follows me. What am I?",
        "answers": ["Flying spaghetti monsters with emotional baggage", "A flying fish", "A plane"],
        "correct_answer": "Flying spaghetti monsters with emotional baggage",
    },
]


@app.route("/", methods=["GET"])
def index():
    user_name=request.args.get("user_name")
    session["user_name"] = user_name
    return render_template('index.html',
                           user_name=user_name)


@app.route('/question',methods = ["GET","POST"])
def get_riddle():
    if "count" not in session:
        session["count"]=0

    if session["count"]==4:
        session["count"]=0

    if request.method=="GET":
        session["count"]+=1
        riddle = random.choice(riddles)
        index=riddles.index(riddle)
        session["riddle"]=riddle
        riddles.pop(index)
        return render_template('get_riddle.html',
                        riddle=riddle,
                        count=session["count"])
    elif request.method=="POST":
        user_name=session.get("user_name")
        selected_answer=request.form["answer"]
        riddle=session.get("riddle")
        correct_answer=riddle["correct_answer"]
        if selected_answer == correct_answer:
            feedback = "Congratulations! You got the answer right!"
        else:
            feedback = "Sorry, that's not the right answer. Try again!"
            return render_template(
                "get_riddle.html",
                user_name=user_name,
                riddle=riddle,
                answer=selected_answer,
                correct_answer=correct_answer,
                feedback=feedback,
                count=session["count"]
                
            )
        
    return render_template(
        "get_riddle.html",
        user_name=user_name,
        riddle=riddle,
        answer=selected_answer,
        correct_answer=correct_answer,
        feedback=feedback,
        count=session["count"]
    )


@app.route('/end', methods=["GET"])
def print_end():
    return render_template(
        "get_riddle.html",
    )

 

if __name__ == "__main__":
    app.run(debug=True)

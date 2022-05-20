from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys
 
app = Flask(__name__)
app.config["SECRET_KEY"]= 'nah'
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


responses = []
satisfaction = surveys["satisfaction"]

current_question = 0
MAX_LENGTH = len(satisfaction.questions)


@app.route("/")
def show_starting_page():

    return render_template("start.html", satisfaction= satisfaction, current_question=current_question)



@app.route("/question/<int:question_number>")
def show_next_question(question_number):
    if question_number > current_question:
        flash("You are trying to access an invalid url")
        return redirect(f"/question/{current_question}")

    elif question_number >= MAX_LENGTH: 
        flash("You are trying to access an invalid url")
        return redirect("/thank_you")
    elif current_question == MAX_LENGTH:
        flash("You are trying to access an invalid url")
        return redirect("/thank_you")
    
    return render_template("question.html", current_question=current_question, satisfaction=satisfaction)



@app.route("/answer", methods = ["POST"])
def store_answer():
    global current_question 
    if current_question >= MAX_LENGTH:
        
        return redirect("/thank_you")
    

    responses.append(request.form["question"])
    
    current_question += 1
    
    return redirect(f"question/{current_question}" if current_question < MAX_LENGTH else "/thank_you")

@app.route("/thank_you")
def show_thanks():
    if current_question < MAX_LENGTH:
        ("You are trying to access an invalid url")
        return redirect(f"question/{current_question}")
    return render_template("thankyou.html")
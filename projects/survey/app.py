#see note on base.html about template structure


from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys
 
app = Flask(__name__)
app.config["SECRET_KEY"]= 'nah'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

satisfaction = surveys["satisfaction"]
MAX_LENGTH = len(satisfaction.questions) # variable for readability
# var to track the furthest question the user has gotten up to
current_question = 0 
#var to read the question the user wants to see, in case they want to go back to change an answer
question_num = None



@app.route("/")
def show_starting_page():

    return render_template("start.html", satisfaction= satisfaction, current_question=current_question)

#start html routes to this url
@app.route("/initialize_survey", methods = ["POST"])
def initialize_survey():
    """reset survey by clearing out responses and setting current question to 0 """
    global current_question
    current_question = 0

    #stores list of user responses in flask session
    session['responses'] = []
    
    return redirect(f"/question/{current_question}")


@app.route("/question/<int:question_number>")
def show_next_question(question_number):
    """display a question, based on a url var, as long as the survey hasn't been completed"""

    #if the survey isn't completed yet
    if current_question < MAX_LENGTH:

        #user is redirected if the try to answer a question that doesn't exist, or that they haven't gotten to yet
        if question_number > current_question:
            flash("You are trying to access an invalid url")
            return redirect(f"/question/{current_question}")

   #the user is redirected if the try to view any question once the survey is over
    elif current_question >= MAX_LENGTH:
        flash("You are trying to access an invalid url")
        return redirect("/thank_you")
    #changes the global var, so that answer view func knows if a question has been answered yet
    global question_num
    question_num = question_number
    return render_template("question.html",question_number=question_number , current_question=current_question, satisfaction=satisfaction)


#only accessed by the question html form sending a post request to this route
@app.route("/answer", methods = ["POST"])
def store_answer():
    """update flask session data and redirect to next question or thank you page"""
    global current_question 
    global question_num
    
    #session data is copied to a list so it can be modified and updated
    resp = session["responses"]
    number = question_num
    #if the question has already been answered, in which case, the user is revisiting an earlier Q to change their answer
    if (len(resp) > number):
        #remove the previous ans, and replace it so that the responses length stays consistent
        resp.pop(number)
        resp.insert(number, request.form["question"])
    else:
        resp.append(request.form["question"])
    session["responses"] = resp
    
    #updates the current Q the user should be up to
    current_question = len(session["responses"] )
    
    return redirect(f"question/{current_question}" if current_question < MAX_LENGTH else "/thank_you")

#accessed by the answer route, if the survey has been completed
@app.route("/thank_you")
def show_thanks():
    """thank the user for taking the time to respond to the survey"""

    #stops user from accessing route prematurely
    if current_question < MAX_LENGTH:
        ("You are trying to access an invalid url")
        return redirect(f"question/{current_question}")
    return render_template("thankyou.html")
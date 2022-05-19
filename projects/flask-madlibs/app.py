from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from stories import story

app = Flask(__name__)
app.config["SECRET_KEY"] = "nope"

debug = DebugToolbarExtension(app)

@app.route("/")
def show_landing():
    blanks = story.prompts
    return render_template("home.html", prompts=blanks)

@app.route("/story")
def show_madlib():
    answer = {prompt:request.args.get(f"{prompt}") for prompt in story.prompts }
    madlib = story.generate(answer)
    
    return render_template("story.html", madlib=madlib)


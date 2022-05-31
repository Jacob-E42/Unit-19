"""define a server that runs a boggle game borrowing functionality from boggle.py"""

from boggle import Boggle
from flask import Flask, request, redirect, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "nooo"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()



@app.route("/")
def show_home():
    """Render a starting page which gives instructions to the user"""    

    return render_template("index.html")


@app.route("/play")
def play_game():
    """load the game board and initialize all of the variables the game tracks"""

    board = boggle_game.make_board()
    session['board'] = board
    session['times_played'] = session.get("times_played", 0) + 1
    session['highest_score'] = session.get('highest_score', 0)
    
    
    return render_template("board.html", board=board)

@app.route("/real_word")
def is_real_word():
    """Take a word from user input and return a json response about the status of the words validity"""

    word = request.args['word']
    board = session['board']
    resp = boggle_game.check_valid_word(board, word)

    return jsonify({"result": resp})
    


@app.route("/end_game", methods=["POST"])
def end_game():
    """take in the final score from the game and update the highscore and the number of times played"""

    score = request.json["score"]
    highscore = session.get('highest_score', 0)

    session['highest_score'] = max(score, highscore)
    session['times_played'] += 1
    return redirect("/play")
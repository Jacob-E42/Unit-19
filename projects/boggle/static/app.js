"use strict";

const $board = $("#board");
const $form = $('#form');
const $input = $('#input');
const $submitButton = $('#submit');
const $messageArea = $('#message');
const $stats = $('#stats')
const BASE_URL = "http://127.0.0.1:5000"

let boggle;
let $currentScore = $("<p>")

//function that runs when DOM is loaded, it creates a new Game instance, puts event handlers on the form
// and sets a timeout to end the game in 60 seconds.
async function startGame() {
    console.debug("startGame")
    boggle = new Game();
    $stats.prepend($currentScore)

    const timeout = setTimeout(endGame, 60000);
    $submitButton.on('click', (e) => e.preventDefault());
    $submitButton.on('click', handleWord);
}

//func that runs when the user tries to submit a word. It uses a Game instance method to check the validity 
// of the guess word. Depending on the result a different a different message is displayed to the user.
// If the word is a good guess, then the score is updated. At the end the current score is updated for the user to see.
async function handleWord() {
    console.debug("handleWord");
    const word = $input.val();
    const resp = await boggle.validateWord(word);


    if (resp === "not-a-word") {
        displayMessage("That is not a valid word")
    }
    else if (resp === "not-on-board") {
        displayMessage("This word is not on the board")
    }
    else if (resp === 'ok') {
        const isNewGuess = boggle.isNotDuplicate(word);
        if (isNewGuess) {
            boggle.calculateScore(word);
            boggle.guessedWords.add(word)
            displayMessage("Nice! That's a new word!")
        }
        else {
            displayMessage("You can't guess a word twice")
        }
    }


    $currentScore.text(`Current Score: ${boggle.score}`)

}

//ends the game and stops the user from guessing new words. The final score of the game is sent back to the api. 
function endGame() {
    console.debug("endGame");
    $submitButton.off("click", handleWord);
    boggle.postHighScore();
    displayMessage("The Game is over! Press the new game button to begin a new game.");
}

//appends a new p to the DOM with whatever message is passed in
function displayMessage(msg) {
    console.debug("displayMessage")
    const $newP = `<p class="message"> ${msg}</p>`
    setTimeout(() => $messageArea.empty(), 5000)
    $messageArea.append($newP)
}


$(startGame);

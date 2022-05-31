/* Define the main data structure that app.js uses. A game instance only tracks the current score of the game
    and which words were guessed already. The board itself is presumed to be provided by the server.

*/

class Game {
    constructor(){
        
        this.score = 0
        this.guessedWords = new Set()
    }

    //take a user provided word and make a request to the server. The server responds with a str explaining the validity
     async validateWord(word) {
        console.debug("validateWord")
        
        const resp = await axios({
            url: `${BASE_URL}/real_word`,
            method: "GET",
            params: {word: word}
        })
        
        return resp.data.result
    }

    //Make sure that the guessed word isn't already in the set of guessed words
    isNotDuplicate(word){
        console.debug("isNotDuplicate")
        if (this.guessedWords.has(word)){
            
            return false
        }
            
        else 
            return true
    }

    //update the current score based on the length of the correctly guessed word
    calculateScore(word){
        console.debug("calculateScore")
        const points = word.length
        this.score += points
    }

    //send a post request to the server offering the final score of this game
    async postHighScore(){
        console.debug("postHighScore")
        const resp = await axios({
            url: `${BASE_URL}/end_game`,
            method: "POST",
            data: {"score": this.score}

        })
        return "Score sent"
    }
}
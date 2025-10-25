from app.models import GameState

def process_guess(guess_type: str, guess: str, game_state: GameState):
    
    if guess_type == "LETTER":
        if guess in game_state.word_array:
            for i in range(0, len(game_state.word_array)):
                if guess == game_state.word_array[i]:
                    game_state.word_progress[i] = guess
        else:
            game_state.lives -= 1
        

    if guess_type == "WORD":
        if guess == game_state.word:
            for i in range(0, len(game_state.word_array)):
                game_state.word_progress[i] = guess[i]
        else:
            game_state.lives -= 1

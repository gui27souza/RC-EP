from ...models import GameState

def process_guess(guess_type: str, guess: str, game_state: GameState):
    
    if guess_type == "LETTER":

        if guess in game_state.word_array:
            pass
        else:
            pass
        

    if guess_type == "WORD":
        
        if guess == game_state.word:
            pass
        else:
            pass
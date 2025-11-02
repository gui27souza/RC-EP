debug = False

def print_debug(message: str):
    if debug:
        print('\n'+'='*4+" DEBUG "+'='*4)
        print(message+'\n')

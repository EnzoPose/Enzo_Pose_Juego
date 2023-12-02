DEBUG = False

def change_mode():
    global DEBUG
    DEBUG = not DEBUG

def get_mode():
    return DEBUG

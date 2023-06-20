import random

excited_lines = [
    "Insert your own line here"
]

not_so_excited_lines = [
    "Insert your own line here"
]

def get_excited_line():
    return random.choice(excited_lines)

def get_sad_line():
    return random.choice(not_so_excited_lines)
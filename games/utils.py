import random

def get_random_cards():
    cards = random.sample(range(1, 11), 5)
    return sorted(cards) 
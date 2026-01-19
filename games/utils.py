# games/utils.py
import random

def get_random_cards():
    """
    1부터 10 사이의 숫자 중 중복 없이 5개의 숫자를 리스트로 반환합니다.
    """
    return random.sample(range(1, 11), 5)
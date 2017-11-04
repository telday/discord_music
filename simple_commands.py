"""
    file: simple_commands.py
    author: Ellis Wright
    language: python 3.6
    description: Logic for some simple commands in discord bot
"""
from random import choice, seed
from time import time
def roll_die_l(minimum, maximum):
    """
        NatNum * NatNum -> NatNum
        Returns a number between min and max
    """
    seed(time())
    return choice(range(minimum, maximum + 1))

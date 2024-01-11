import os
from typing import List, Dict
import random


def info_str(center_content: str = "", 
            side_str: str = "=", 
            side_num: int = 25) -> str:
    return "\n" + \
        side_str * side_num + " " + \
        center_content + " " + \
        side_str * side_num + \
        "\n"

def show_cards(
        cards: Dict[str, str], 
        type: str = 'model', 
        num: int = 1, 
        sample: str = 'head'
    ):
    """Show the model cards for a number of `num` with the sample strategy `sample`
    where `sample` can be 'head', 'tail', 'random', etc
    """
    if sample == 'head':
        cards_sample = list(cards.keys())[:num]
    elif sample == 'tail':
        cards_sample = list(cards.keys())[-num:]
    elif sample == 'random':
        cards_sample = random.sample(list(cards.keys()), num)
    else:
        raise ValueError(f"Invalid sample strategy: {sample}")
        
    for key in cards_sample:
        print(info_str(f"The {type} card for the repo address: {key}"))
        print(cards[key])
        print()
    
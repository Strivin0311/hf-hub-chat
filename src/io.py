import os
import json
from typing import List, Dict

def load_json(
        save_path: str
    ):
    """Load the json file
    """
    with open(save_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
    
def save_json(
        json_obj,
       save_path: str 
    ):
    """Save the json file
    """
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(json_obj, f, ensure_ascii=False)


def load_id_list(
        data_root: str = "data",
        type: str = 'model',
    ) -> List[str]:
    """Load the id list from the json file
    """
    load_path = os.path.join(data_root, f"{type}_ids.json")

    print(f"Loading the {type} id list from {load_path}")
    
    return load_json(load_path)
    

def save_id_list(
        id_list: List[str],
        data_root: str = "data",
        type: str = 'model',
        overwrite: bool = False
    ) -> None:
    """Save the id list to the json file
    """
    save_path = os.path.join(data_root, f"{type}_ids.json")

    if not overwrite and os.path.exists(save_path):
        old_id_list = load_id_list(data_root, type)
        id_list = list(set(id_list) + set(old_id_list))

    save_json(id_list, save_path)

    print(f"Saved the {type} id list to {save_path}")


def load_failed_pages(
        data_root: str = "data",
    ) -> List[int]:
    """Load the failed pages from the json file
    """
    load_path = os.path.join(data_root, f"{type}_failed_pages.json")

    print(f"Loading the {type} failed pages from {load_path}")

    return load_json(load_path)


def save_failed_pages(
        failed_pages: List[int],
        data_root: str = "data",
    ) -> None:
    """Save the failed pages to the json file
    """
    save_path = os.path.join(data_root, f"{type}_failed_pages.json")

    save_json(failed_pages, save_path)

    print(f"Saved the {type} failed pages to {save_path}")


def load_cards(
        data_root: str = "data",
        type: str = 'model',
    ) -> List[str]:
    """Load the model cards from the json file
    """
    load_path = os.path.join(data_root, f"{type}_cards.json")

    print(f"Loading the {type} cards from {load_path}")

    return load_json(load_path)
    

def save_cards(
        cards: Dict[str, str],
        data_root: str = "data",
        type: str = 'model',
        overwrite: bool = False
    ) -> None:
    """Save the model cards to the json file
    """
    save_path = os.path.join(data_root, f"{type}_cards.json")

    if not overwrite and os.path.exists(save_path):
        old_cards = load_cards(data_root, type)
        cards = {**old_cards, **cards}

    save_json(cards, save_path)

    print(f"Saved the {type} cards to {save_path}")


def load_failed_repos(
        data_root: str = "data",
    ) -> List[int]:
    """Load the failed repos from the json file
    """
    load_path = os.path.join(data_root, f"{type}_failed_repos.json")

    print(f"Loading the {type} failed repos from {load_path}")

    return load_json(load_path)
    

def save_failed_repos(
        failed_repos: List[int],
        data_root: str = "data",
    ) -> None:
    """Save the failed repos to the json file
    """
    save_path = os.path.join(data_root, f"{type}_failed_repos.json")

    save_json(failed_repos, save_path)

    print(f"Saved the {type} failed repos to {save_path}")


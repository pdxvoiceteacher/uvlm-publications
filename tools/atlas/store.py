import json
import os


def store_card(card):
    os.makedirs("atlas_store", exist_ok=True)

    path = f"atlas_store/{card['title'].replace(' ', '_')}.json"

    with open(path, "w") as f:
        json.dump(card, f, indent=2)

    return path

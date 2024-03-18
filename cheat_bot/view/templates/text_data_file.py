import json


def get_text_data_from_json():
    with open('cheat_bot/view/templates/text_data_file.json', 'r') as f:
        return json.load(f)


text_data = get_text_data_from_json()

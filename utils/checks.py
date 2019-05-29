import json


def load_optional_config():
    with open('settings/optional_config.json', 'r') as f:
        return json.load(f)


def embed_perms(message):
    try:
        check = message.author.permissions_in(message.channel).embed_links
    except:
        check = True

    return check

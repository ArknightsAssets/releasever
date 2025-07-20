import urllib.error
import urllib.request
import json

def fetch_current_version() -> str:
    with urllib.request.urlopen("https://ak-conf.hypergryph.com/config/prod/official/Android/version") as response:
        return json.loads(response.read())["resVersion"]


def fetch_hot_update_list(version: str):
    with urllib.request.urlopen(f"https://ak.hycdn.cn/assetbundle/official/Android/assets/{version}/hot_update_list.json") as response:
        return json.loads(response.read())

def get_characters_in_version(version: str) -> list[str]:
    try:
        hol = fetch_hot_update_list(version)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        raise

    characters: list[str] = []
    for info in hol["abInfos"]:
        if info["name"].startswith("charpack/char_"):
            characters.append(info["name"].split("/", 1)[1].split(".", 1)[0])
    
    return characters


with open("releasever.json") as file:
    releasever: dict[str, str] = json.load(file)

current_version = fetch_current_version()
for character in get_characters_in_version(current_version):
    if character not in releasever:
        releasever[character] = current_version

with open("releasever.json", "w") as file:
    json.dump(releasever, file, indent=4)

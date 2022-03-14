import json
from typing import Dict, List
from xml.etree.ElementTree import Element, parse


def parse_xml(files: List[str]) -> List[Dict[str, str]]:
    roots = [parse(file).getroot() for file in files]
    monsters = list()
    for root in roots:
        monsters += [monster for monster in root]

    converted_monsters = list()
    for monster in monsters:
        converted_monsters.append(parse_monster(monster))
    return converted_monsters


def parse_monster(monster: Element) -> Dict[str, str]:
    converted_monster = dict()
    converted_monster["title"] = monster.find("name").text
    converted_monster["icon"] = "imp-laugh"
    converted_monster["contents"] = get_content_list(monster)
    return converted_monster


def get_content_list(monster: Element) -> List[str]:
    return [
        f"subtitle | "
        f"{translate_size(monster.find('size').text)} "
        f"{monster.find('type').text.split(',')[0]}",
        f"rule",
        f"property | Alignment | {monster.find('alignment').text}",
        f"rule",
        f"property | Armor class | {monster.find('ac').text}",
        f"property | Hit points | {monster.find('hp').text}",
        f"property | Speed | {monster.find('speed').text}",
        f"rule",
        f"dndstats | {monster.find('str').text} | {monster.find('dex').text} | "
        f"{monster.find('con').text} | {monster.find('int').text} | {monster.find('wis').text} | "
        f"{monster.find('cha').text}",
        f"rule",
        f"property | Saving Throws | {monster.find('save').text}",
        f"property | Skills | {monster.find('skill').text}",
        f"property | Senses | {monster.find('senses').text}",
        f"property | Languages | {monster.find('languages').text}",
        f"property | Challenge | {monster.find('cr').text}"
    ]


def translate_size(size: str) -> str:
    sizes = {
        "T": "Tiny",
        "S": "Small",
        "M": "Medium",
        "L": "Large",
        "H": "Huge",
        "G": "Gargantuan",
    }
    return sizes[size]


def shorten_alignment(alignment: str) -> str:
    return alignment.split(" alignment")[0]


if __name__ == "__main__":
    monster_xmls = ["c:/users/maelic/downloads/volo.xml",
                    "c:/users/maelic/downloads/MToF Beastiary.xml"]

    json_data = parse_xml(monster_xmls)
    with open("monsters.json", "w") as save_file:
        json.dump(json_data, save_file, indent=2)

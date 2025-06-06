from dataclasses import dataclass
import logging
from typing import Literal
import requests

HEART: Literal["♥"] = "♥"
MIND: Literal["🧠"] = "🧠"
HTML_URL = "https://devrel.wearedevelopers.com/code100-puzzles/041-hearts-and-minds/hearts-and-minds.html"

type Icon = Literal["♥", "🧠"]


@dataclass
class Placement:
    rotation: int
    left_offset: int
    icon: Icon

    def is_straight(self) -> bool:
        return self.rotation in (0, 90, 180, 270)


def extract_placement(line: str, icon: Icon) -> Placement | None:
    try:
        rotation = int(line.split("rot-")[1].split(" ")[0])
        left_offset = int(line.split("left-")[1].split(" ")[0])
        return Placement(rotation, left_offset, icon)
    except Exception as e:
        logging.error(f"Error extracting rotation: {e}")
        return None


def calculate_center(placements: list[Placement]) -> float:
    min_left = min(map(lambda p: p.left_offset, placements))
    max_left = max(map(lambda p: p.left_offset, placements))
    return (min_left + max_left) / 2


def run_challenge(html_str: str) -> None:
    hearts = []
    minds = []
    for line in html_str.split("\n"):
        if HEART in line:
            placement = extract_placement(line, HEART)
            if placement:
                hearts.append(placement)
        elif MIND in line:
            placement = extract_placement(line, HEART)
            if placement:
                minds.append(placement)

    center = calculate_center(hearts + minds)

    minds_left_of_center = sum([1 if m.left_offset < center else 0 for m in minds])
    hearts_right_of_center = sum([1 if h.left_offset > center else 0 for h in hearts])
    straight_hearts = sum([1 if h.is_straight() else 0 for h in hearts])
    straight_minds = sum([1 if m.is_straight() else 0 for m in minds])

    print(f"Straight hearts: {straight_hearts}")
    print(f"Straight minds: {straight_minds}")
    print(f"Moinds left of center: {minds_left_of_center}")
    print(f"Hearts right of center: {hearts_right_of_center}")


if __name__ == "__main__":
    response = requests.get(HTML_URL)
    html_str = response.text

    run_challenge(html_str)

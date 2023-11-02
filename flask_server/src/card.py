from dataclasses import dataclass
from typing import Set, Tuple


@dataclass
class Card:
    cost: int
    energy: int
    type: str
    subtype: Set[str]
    points: int
    image: str
    name: str
    description: str
    rarity: str
    keywords: Set[Tuple[str, ...]]

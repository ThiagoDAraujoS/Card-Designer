from dataclasses import dataclass
from typing import Set, Tuple, List


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


class Bank:
    cards: List[Card] = []

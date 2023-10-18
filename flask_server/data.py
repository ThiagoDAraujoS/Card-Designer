from dataclasses import dataclass, field
from typing import Set, Tuple, List
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Card:
    cost: int = 0
    energy: int = 0
    type: str = "no type"
    subtype: Set[str] = field(default_factory=set)
    points: int = 0
    image: str = "no image"
    name: str = "no name"
    description: str = "no description"
    rarity: str = "common"
    keywords: Set[Tuple[str, ...]] = field(default_factory=set)


@dataclass_json
@dataclass
class Bank:
    cards: List[Card] = field(default_factory=list)

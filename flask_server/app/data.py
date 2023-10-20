from dataclasses import dataclass, field
from typing import Set, Tuple
from dataclasses_json import dataclass_json
import uuid


@dataclass_json
@dataclass
class Card:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
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

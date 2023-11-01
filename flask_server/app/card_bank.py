import os
from dataclasses import dataclass, field
from typing import Dict

from dataclasses_json import dataclass_json
from os import path

from flask_server.app.bank import Bank
from flask_server.app.data import Card
from uuid import uuid4 as generate_uuid
from . import UUIDString, PathString, JsonString


@dataclass_json
@dataclass
class CardBankData:
    """ Data class for managing a collection of cards. """
    cards: Dict[UUIDString, Card] = field(default_factory=dict)
    """ A set of cards contained in the data. """


class CardBank(Bank):
    META_FILE_NAME: str = "card_index.json"
    CACHE_FOLDER_NAME: str = "cards"

    def __init__(self, name, main_path: PathString):
        super().__init__(name, main_path)

    def _data_from_json(self, json_string: JsonString) -> CardBankData:
        return CardBankData.from_json(json_string)

    def _init_data(self) -> CardBankData:
        return CardBankData()

    def get_card_file_path(self, uuid: UUIDString) -> PathString:
        return PathString(path.join(self.cache_path, f"{uuid}.json"))

    def create_card(self, json_string: JsonString) -> Card:
        uuid = UUIDString(str(generate_uuid()))
        card_path = self.get_card_file_path(uuid)
        new_card = Card.from_json(json_string)
        with open(card_path, 'w') as card_file:
            card_file.write(new_card.to_json())
        self.data.cards[uuid] = new_card
        return new_card

    def delete_card(self, uuid: UUIDString) -> None:
        if uuid not in self.data.cards:
            raise Exception("Card UUID not existent in card bank data")
        card_path = self.get_card_file_path(uuid)
        if not path.exists(card_path):
            raise Exception("Card file missing")

        self.data.cards.pop(uuid)
        os.remove(self.get_card_file_path(uuid))

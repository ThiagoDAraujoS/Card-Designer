from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json

from flask_server.app.bank import Bank
from flask_server.app.data import Card


@dataclass_json
@dataclass
class Data:
    """ Data class for managing a collection of cards. """
    cards: List[Card] = field(default_factory=list)
    """ A set of cards contained in the data. """


class CardBank(Bank):
    META_FILE_NAME: str = "card_index.json"
    CACHE_FOLDER_NAME: str = "cards"

    def __init__(self, name, main_path):
        super().__init__(name, main_path)
        pass

    def _data_from_json(self, json_string) -> Data:
        return Data.from_json(json_string)

    def _init_data(self) -> Data:
        return Data()

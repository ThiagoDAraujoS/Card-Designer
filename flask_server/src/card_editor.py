import os
from uuid import uuid4 as generate_uuid
from uuid import UUID

from typing import List

from flask_server.src import Uuid, Json
from flask_server.src.card_set import CardSet, SETTINGS_FILE_NAME


class CardEditor:
    """ This class is able to create and edit cards within a card set """
    def __init__(self):
        self.card_set: CardSet | None = None
        """ The editor will edit cards within this set """

    def scope_to_set(self, card_set: CardSet):
        self.card_set = card_set

    def create_card(self, card_data: Json) -> Uuid:
        """ Create a new card file and stash it """
        card_uuid = str(generate_uuid())
        card_path = os.path.join(self.card_set.path, f"{card_uuid}.json")
        with open(card_path, 'w') as file:
            file.write(card_data)
        return Uuid(card_uuid)

    def update_card(self, card_uuid: Uuid, card_data: Json) -> None:
        """ Update an existing card """
        card_path = os.path.join(self.card_set.path, f"{card_uuid}.json")
        if not os.path.exists(card_path):
            raise FileNotFoundError("CARD_SET UPDATE_CARD - Missing card file")
        with open(card_path, 'w') as file:
            file.write(card_data)

    def get_card_data(self, card_uuid: UUID) -> Json:
        """ Get cards data """
        card_path = os.path.join(self.card_set.path, f"{card_uuid}.json")
        if not os.path.exists(card_path):
            raise FileNotFoundError("CARD_SET UPDATE_CARD - Missing card file")
        with open(card_path, 'r') as file:
            return Json(file.read())

    def get_card_list(self) -> List[UUID]:
        """ Get a list with all cards in this set """
        cards = []
        for file in os.listdir(self.card_set.path):
            if not os.path.isfile(os.path.join(self.card_set.path, file)) or file == SETTINGS_FILE_NAME:
                continue
            name, _ = os.path.splitext(file)
            cards.append(UUID(name))
        return cards

    def get_changed_cards(self) -> List[UUID]:
        """ Get all files that have been changed but not saved """
        result = []
        for card in self.card_set.repo.index.diff(None):
            card = card.b_path
            if not os.path.isfile(os.path.join(self.card_set.path, card)) or card == SETTINGS_FILE_NAME:
                continue
            name, _ = os.path.splitext(card)
            result.append(UUID(name))
        return result

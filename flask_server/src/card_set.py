"""
This script describes a card set, card sets contain many card files and are controlled by GIT
"""

import git
import os
from uuid import uuid4 as generate_uuid
from uuid import UUID

from flask_server.src import Json, Path, Uuid, Save
from typing import NewType, List


SETTINGS_FILE_NAME = "settings.json"


class CardSet:
    def __init__(self, path: Path, repo: git.Repo):
        """ Initialize a CardSet object """
        self.path: Path = path
        self.repo: git.Repo = repo

    @staticmethod
    def create_repo(path):
        repo = git.Repo.init(path)
        open(os.path.join(path, SETTINGS_FILE_NAME), "wb").close()
        repo.index.add("*")
        repo.index.commit("Project has started")
        return repo

    def save_changes(self, message: str):
        # Get the current branch name
        branch_name = self.repo.active_branch.name

        # Get the hash of the current commit
        commit_hash = self.repo.head.commit.hexsha

        # Shelve changes
        self.repo.git.stash("save", "-u")

        # Switch to the head of the current branch
        self.repo.heads[branch_name].checkout()

        # Hard reset the branch to the specified commit
        self.repo.git.reset("--hard", commit_hash)

        # Unshelve changes
        self.repo.git.stash("pop")

        # Stage changes
        self.repo.index.add("*")

        # Commit the changes
        self.repo.git.commit("-m", message)

    def create_save_file(self, name: Save, message: str):
        """ Create a new save_file or branch and push the current changes to this new save_file """
        if name in [branch.name for branch in self.repo.heads]:
            raise ValueError(f"CARD_SET SAVE - Save state '{name}' already exists.")
        self.repo.create_head(name)
        self.repo.heads[name].checkout()
        self.save_changes(message)

    def get_save_files(self):
        return [branch.name for branch in self.repo.heads]

    def delete_save_file(self, name: Save):
        """ Delete a save file """
        self.repo.git.branch("-D", name)

    def rollback(self):
        """ Rollback the current changes """
        self.repo.git.reset("--hard", "HEAD^")

    def load_save_file(self, name: Save):
        """ Checks out a save branch """
        self.repo.git.checkout(name, force=True)

    def load_commit(self, commit_hash):
        """ Load a targeted commit """
        self.repo.git.checkout(commit_hash, force=True)

    def create_card(self, card_data: Json) -> Uuid:
        """ Create a new card file and stash it """
        card_uuid = str(generate_uuid())
        card_path = os.path.join(self.path, f"{card_uuid}.json")
        with open(card_path, 'w') as file:
            file.write(card_data)
        return Uuid(card_uuid)

    def update_card(self, card_uuid: Uuid, card_data: Json) -> None:
        """ Update an existing card """
        card_path = os.path.join(self.path, f"{card_uuid}.json")
        if not os.path.exists(card_path):
            raise FileNotFoundError("CARD_SET UPDATE_CARD - Missing card file")
        with open(card_path, 'w') as file:
            file.write(card_data)

    def fetch_card(self, card_uuid: UUID) -> Json:
        """ Get cards data """
        card_path = os.path.join(self.path, f"{card_uuid}.json")
        if not os.path.exists(card_path):
            raise FileNotFoundError("CARD_SET UPDATE_CARD - Missing card file")
        with open(card_path, 'r') as file:
            return Json(file.read())

    def get_card_list(self) -> List[UUID]:
        cards = []
        for file in os.listdir(self.path):
            if not os.path.isfile(os.path.join(self.path, file)) or file == SETTINGS_FILE_NAME:
                continue
            name, _ = os.path.splitext(file)
            cards.append(UUID(name))
        return cards

    def get_changed_cards(self) -> List[UUID]:
        result = []
        for card in self.repo.index.diff(None):
            card = card.b_path
            if not os.path.isfile(os.path.join(self.path, card)) or card == SETTINGS_FILE_NAME:
                continue
            name, _ = os.path.splitext(card)
            result.append(UUID(name))
        return result

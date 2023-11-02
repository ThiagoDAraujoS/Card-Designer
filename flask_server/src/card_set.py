"""
This script describes a card set, card sets contain many card files and are controlled by GIT
"""

import git
import os
from uuid import uuid4 as generate_uuid
from uuid import UUID

from flask_server.src import Json, Path, Uuid, Save
from typing import NewType


class CardSet:
    def __init__(self, path: Path, repo: git.Repo):
        """ Initialize a CardSet object """
        self.path: Path = path
        self.repo: git.Repo = repo

    @staticmethod
    def create_repo(path):
        repo = git.Repo.init(path)
        open(os.path.join(path, "settings.json"), "wb").close()
        repo.index.add("*")
        repo.index.commit("Project has started")
        return repo

    def commit_changes(self, message: str):
        """ This method force commits all the changes to its branch """
        self.repo.index.add("*")
        self.repo.git.commit("-q", "--force", "-m", message)

    def create_save_file(self, name: Save, message: str):
        """ Create a new save_file or branch and push the current changes to this new save_file """
        if name in [branch.name for branch in self.repo.heads]:
            raise ValueError(f"CARD_SET SAVE - Save state '{name}' already exists.")
        self.repo.create_head(name)
        self.repo.heads[name].checkout()
        self.commit_changes(message)

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

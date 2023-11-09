import git
import os
from uuid import uuid4 as generate_uuid
from uuid import UUID

from flask_server.src import Json, Path, Uuid, Branch
from typing import List


SETTINGS_FILE_NAME = "settings.json"


class CardSet:
    """ This script describes a card set, card sets contain many card files and are controlled by GIT """
    def __init__(self, path: Path, repo: git.Repo):
        """ Initialize a CardSet object """
        self.path: Path = path
        self.repo: git.Repo = repo

    @staticmethod
    def create_repo(path):
        """ Create a repo for this card set, this is designed to be used by the registry"""
        repo = git.Repo.init(path)
        open(os.path.join(path, SETTINGS_FILE_NAME), "wb").close()
        repo.index.add("*")
        repo.index.commit("Project has started")
        return repo

    def get_active_branch(self) -> Branch:
        return Branch(self.repo.active_branch.name)

    def save_changes(self, message: str):
        """ Commit the changes to this branch """
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

    def create_branch(self, name: Branch, message: str):
        """ Create a new save_file or branch and push the current changes to this new save_file """
        if name in [branch.name for branch in self.repo.heads]:
            raise ValueError(f"CARD_SET SAVE - Save state '{name}' already exists.")
        self.repo.create_head(name)
        self.repo.heads[name].checkout()
        self.save_changes(message)

    def get_branches(self):
        """ Get a list of all saved files """
        return [branch.name for branch in self.repo.heads]

    def delete_branch(self, name: Branch):
        """ Delete a branch """
        self.repo.git.branch("-D", name)

    def rollback(self):
        """ Rollback the current changes """
        self.repo.git.reset("--hard", "HEAD^")

    def load_branch(self, name: Branch):
        """ Checks out a save branch """
        self.repo.git.checkout(name, force=True)

    def load_commit(self, commit_hash):
        """ Load a targeted commit """
        self.repo.git.checkout(commit_hash, force=True)

    def get_commit_list(self, branch_name):
        branch = self.repo.heads[branch_name]
        commit_list = [(commit.hexsha, commit.message) for commit in branch.commit.iter_parents()]
        return commit_list

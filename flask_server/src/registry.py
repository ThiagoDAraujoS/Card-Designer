import stat
from typing import List
import os
import shutil
import git
import subprocess

from flask_server.src import Path, Project
from flask_server.src.card_set import CardSet


class Registry:
    """ This class manipulate card set projects """
    def __init__(self, registry_path: Path):
        self.path = registry_path

    def _get_git_repo(self, name: Project) -> git.Repo | None:
        """ Return the git repo object out of a folder within the registry """
        folder_path = os.path.join(self.path, name)

        if not os.path.exists(folder_path):
            raise FileNotFoundError("REGISTRY GET_PROJECT - Project does not exist in registry")

        try:
            return git.Repo(folder_path)
        except git.InvalidGitRepositoryError:
            return None

    def get_project_names(self) -> List[Project]:
        """ Return a list with all valid projects inside the registry """
        projects = []
        for folder_name in os.listdir(self.path):
            if not os.path.isdir(os.path.join(self.path, folder_name)):
                continue

            if self._get_git_repo(Project(folder_name)):
                projects.append(Project(folder_name))

        return projects

    def create_project(self, name: Project) -> git.Repo:
        """ Create a new project and set up a git repo for it """
        folder_path = os.path.join(self.path, name)

        if os.path.exists(folder_path):
            raise FileExistsError("REGISTRY NEW_PROJECT - Project folder already exists in registry")

        os.mkdir(folder_path)
        return CardSet.create_repo(folder_path)

    def delete_project(self, name: Project) -> None:
        """ Delete a project in the registry """
        folder_path = os.path.join(self.path, name)

        if not os.path.exists(folder_path):
            raise FileNotFoundError("REGISTRY DELETE - Project does not exist in registry")

        git.rmtree(folder_path)

    def get_project(self, name: Project) -> CardSet:
        """ Return a CardSet project object from the registry """
        project_path = Path(os.path.join(self.path, name))
        return CardSet(project_path, self._get_git_repo(name))

# repo = self._get_git_repo(name)
# repo.close()
# git.rmtree(os.path.join(self.path, name))

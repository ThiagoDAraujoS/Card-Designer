from typing import List
import os
import shutil
import git

from flask_server.src import Path
from flask_server.src.card_set import CardSet


class Registry:
    """ This class manipulate card set projects """
    def __init__(self, registry_path: Path):
        self.path = registry_path

    def _get_git_repo(self, project_name) -> git.Repo | None:
        """ Return the git repo object out of a folder within the registry """
        folder_path = os.path.join(self.path, project_name)

        if not os.path.exists(folder_path):
            raise FileNotFoundError("REGISTRY GET_PROJECT - Project does not exist in registry")

        try:
            return git.Repo(folder_path)
        except git.InvalidGitRepositoryError:
            return None

    def get_project_names(self) -> List[str]:
        """ Return a list with all valid projects inside the registry """
        projects = []
        for folder_name in os.listdir(self.path):
            folder_path = os.path.join(self.path, folder_name)
            if not os.path.isdir(folder_path):
                continue

            repo = self._get_git_repo(folder_path)
            if repo:
                projects.append(folder_name)

        return projects

    def create_project(self, project_name) -> git.Repo:
        """ Create a new project and set up a git repo for it """
        folder_path = os.path.join(self.path, project_name)

        if os.path.exists(folder_path):
            raise FileExistsError("REGISTRY NEW_PROJECT - Project folder already exists in registry")

        os.mkdir(folder_path)

        return git.Repo.init(folder_path)

    def delete_project(self, project_name) -> None:
        """ Delete a project in the registry """
        folder_path = os.path.join(self.path, project_name)

        if not os.path.exists(folder_path):
            raise FileNotFoundError("REGISTRY DELETE - Project does not exist in registry")

        shutil.rmtree(os.path.join(self.path, project_name))

    def get_project(self, project_name) -> CardSet:
        """ Return a CardSet project object from the registry """
        return CardSet(project_name, self._get_git_repo(project_name))

import os
import shutil
from typing import Tuple

from flask_server.src.card_set import CardSet
from flask_server.src.images import ImageBank
from flask_server.src.registry import Registry
from flask_server.src import Path, Project


class Manager:
    """ This master class manages the overall tool functionalities and folder structures """
    def __init__(self):
        src_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.app_folder: Path = Path(os.path.join(src_folder, "app"))
        self.images_folder: Path = Path(os.path.join(self.app_folder, "images"))
        self.sets_folder: Path = Path(os.path.join(self.app_folder, "card_sets"))
        self.loaded_project: Tuple[Project, CardSet] | None = None
        self.image_bank: ImageBank | None = None
        self.registry: Registry | None = None

    def load_project(self, project: Project):
        self.loaded_project = project, self.registry.get_project(project)

    def install(self):
        """ Build the app's folders """
        if os.path.exists(self.app_folder):
            raise FileExistsError("MANAGER INSTALL - The 'app' folder already exists.")

        os.mkdir(self.app_folder)
        os.mkdir(self.images_folder)
        os.mkdir(self.sets_folder)

    def uninstall(self):
        """ Remove all app's data """
        if not os.path.exists(self.app_folder):
            raise FileNotFoundError("MANAGER UNINSTALL - The 'app' folder does not exist.")

        shutil.rmtree(self.app_folder)

    def initialize_components(self):
        self.image_bank = ImageBank(self.images_folder)
        self.registry = Registry(self.sets_folder)

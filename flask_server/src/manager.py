import os
import shutil

from flask_server.src.card_set import CardSet
from flask_server.src.images import ImageBank
from flask_server.src.registry import Registry
from flask_server.src.card_editor import CardEditor
from flask_server.src import Path, Project


class Manager:
    """ This master class manages the overall tool functionalities and folder structures """

    def __init__(self):
        # Initialize paths
        src_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.app_folder: Path = Path(os.path.join(src_folder, "app"))
        self.images_folder: Path = Path(os.path.join(self.app_folder, "images"))
        self.sets_folder: Path = Path(os.path.join(self.app_folder, "card_sets"))

        # Declare Key objects variables
        self.image_bank: ImageBank | None = None
        self.registry: Registry | None = None
        self.editor: CardEditor | None = None

        # Forward useful references
        self.project_name: Project | None = None
        self.project: CardSet | None = None

    def load_project(self, project: Project):
        self.project_name = project
        self.project = self.registry.get_project(project)

    def initialize(self):
        """ Build the app's folders if they don't exist """
        if not os.path.exists(self.app_folder):
            os.mkdir(self.app_folder)

        if not os.path.exists(self.images_folder):
            os.mkdir(self.images_folder)

        if not os.path.exists(self.sets_folder):
            os.mkdir(self.sets_folder)

        self.image_bank = ImageBank(self.images_folder)
        self.registry = Registry(self.sets_folder)
        self.editor = CardEditor()

    def uninstall(self):
        """ Remove all app's data """
        if not os.path.exists(self.app_folder):
            raise FileNotFoundError("MANAGER UNINSTALL - The 'app' folder does not exist.")

        shutil.rmtree(self.app_folder)

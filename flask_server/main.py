""" This should just test the src """
import time

from flask_server.src.manager import Manager
from flask_server.src.images import ImageBank, ImageData
from flask_server.src.registry import Registry
from flask_server.src import Path, Project, Json, Save

IMAGE_PATH = Path("C:\\Users\\Thiago\\Desktop\\Portifolio Projects\\Card Designer\\cards\\wallpapersden.com_minimal-hd-landscape_500x500.jpg")

manager = Manager()
manager.install()
image_bank = ImageBank(manager.images_folder)
registry = Registry(manager.sets_folder)

image_uuid, image_data = image_bank.import_image(IMAGE_PATH)
print(str(image_uuid), image_data.__dict__)

image_bank.write_image_metadata(image_uuid, ImageData("test"))
image_data = image_bank.read_image_metadata(image_uuid)
print(image_data.__dict__)

project_name = Project("test_project")
registry.create_project(project_name)

projects = registry.get_project_names()
print(projects)

test_project = registry.get_project(project_name)
print(test_project.get_save_files())
card_uuid = test_project.create_card(Json("{name:Sun Dino,Type:Dino}"))
test_project.create_save_file(Save("SaveFile"), "First Card Was Created")
print(test_project.__dict__)

# registry.delete_project(project_name)
projects = registry.get_project_names()
print(projects)

test_project.update_card(card_uuid, Json("{name:Moon Dino,Type:Dino}"))
print(test_project.get_card_list())
print(test_project.get_changed_cards())
test_project.save_changes("Changed Cards")
print(test_project.get_changed_cards())
print(test_project.repo.index)

""" This should just test the src """
from flask_server.src.manager import Manager
from flask_server.src.images import ImageBank, ImageData
from flask_server.src import Path

IMAGE_PATH = Path("C:\\Users\\Thiago\\Desktop\\Portifolio Projects\\Card Designer\\cards\\wallpapersden.com_minimal-hd-landscape_500x500.jpg")

manager = Manager()
manager.install()

image_bank = ImageBank(manager.images_folder)
image_uuid, image_data = image_bank.import_image(IMAGE_PATH)
print(str(image_uuid), image_data.__dict__)
image_bank.write_image_metadata(image_uuid, ImageData("test"))
image_data = image_bank.read_image_metadata(image_uuid)
print(image_data.__dict__)

manager.uninstall()

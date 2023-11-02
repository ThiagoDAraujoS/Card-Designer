import os
import shutil
from dataclasses import dataclass, field
from typing import Tuple, Dict
from PIL import Image
from dataclasses_json import dataclass_json
from flask_server.app.bank import Bank
from uuid import uuid4 as generate_uuid
from . import UUIDString, PathString, JsonString


@dataclass_json
@dataclass
class ImageData:
    uuid: UUIDString
    name: str


@dataclass_json
@dataclass
class ImageBankData:
    """ Data class for managing a collection of images. """
    images: Dict[UUIDString, ImageData] = field(default_factory=dict)
    """ A dictionary of cards UUIDS as strings to their original name contained in the image-bank.json. """


class ImageBank(Bank):

    META_FILE_NAME: str = "image_index.json"
    CACHE_FOLDER_NAME: str = "images"

    def __init__(self, name, main_path: PathString):
        super().__init__(name, main_path)
        self.resolution: Tuple[int, int] = (512, 512)

    def _init_data(self) -> ImageBankData:
        return ImageBankData()

    def _data_from_json(self, json_string: JsonString) -> ImageBankData:
        return ImageBankData.from_json(json_string)

    @staticmethod
    def is_valid_jpg(image_path: PathString) -> bool:
        try:
            # Try opening the image using PIL
            img = Image.open(image_path)
            # Check if it's a valid JPEG
            return img.format == 'JPEG'
        except Exception as e:
            print("image is not a jpg", e)
            return False

    def assert_image(self, path: PathString) -> None:
        if not self.is_valid_jpg(path):
            raise Exception("Invalid JPEG image")

    def get_image_path(self, uuid: UUIDString) -> PathString:
        return PathString(os.path.join(self.cache_path, uuid))

    def import_image(self, source_path: PathString, name: str = "") -> UUIDString:
        self.assert_image(source_path)

        if not name:
            name = os.path.basename(source_path)
            name = os.path.splitext(name)

        uuid = UUIDString(str(generate_uuid()))
        target_file_path = self.get_image_path(uuid)
        shutil.copy2(source_path, target_file_path)

        self.data.images[uuid] = ImageData(uuid=uuid, name=name)
        self.save()
        print(f"Imported image named {name} from {source_path} to {uuid}")
        return uuid

    def delete_image(self, uuid: UUIDString) -> None:
        if uuid not in self.data.images:
            raise Exception("ID not present in bank")
        os.remove(self.get_image_path(uuid))
        self.data.images.pop(uuid)
        self.save()

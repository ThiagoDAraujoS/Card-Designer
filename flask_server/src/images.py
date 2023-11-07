import os
import shutil

from typing import Dict
from dataclasses import dataclass

from PIL import Image
import piexif

from uuid import uuid4 as generate_uuid
from uuid import UUID
from . import (Path)

from flask_server.src import Json, Uuid


NAME_IMAGE_TAG = "ImageName"
EXIF_TAG_ORIGINAL_RAW_FILE_NAME = 0xc68b
META_0TH = "0th"
META_EXIF = "Exif"
META_GPS = "GPS"


@dataclass
class ImageData:
    """ Data stub used to describe pictures in the image bank """
    file_name: str = ""
    data: Json = "{}"


class ImageBank:
    """
    This script defines a class that is charged of controlling an image bank folder.
    Images can be added to the bank and other functionalities of this tool will use
    these images to build the cards panels
    """
    def __init__(self, image_bank_path: Path):
        self.path: Path = image_bank_path

        if not os.path.exists(image_bank_path):
            raise FileNotFoundError("IMAGE_BANK SETUP - Missing image bank folder")

    def compile_image_list(self) -> Dict[Uuid, ImageData]:
        """ Look for all the images stored in `self.path`, and compile the `self.images` dictionary """
        images = {}

        for file_name in os.listdir(self.path):
            name, extension = os.path.splitext(file_name)

            if not os.path.isfile(file_name) or extension.lower() != ".jpg":
                continue

            try:
                image_uuid: UUID = UUID(name)
                image = self.read_image_metadata(image_uuid)
                images[Uuid(str(image_uuid))] = image

            except ValueError:
                print(f"IMAGE_BANK SETUP - {name}'s file name is not a valid UUID.")
                continue

        return images

    def get_image_path(self, image_uuid: UUID) -> Path:
        """ Return the absolute path of an image within the `self.path` folder """
        return Path(os.path.join(self.path, f"{str(image_uuid)}.jpg"))

    def write_image_metadata(self, image_uuid: UUID, image_data: ImageData):
        """ Write ImageData information to an image metadata stubs """
        exif_dict = {META_0TH: {}, META_EXIF: {}, META_GPS: {}}

        path = self.get_image_path(image_uuid)
        image = Image.open(path)

        exif_dict[META_0TH][EXIF_TAG_ORIGINAL_RAW_FILE_NAME] = image_data.file_name.encode('utf-8')

        exif_bytes = piexif.dump(exif_dict)

        image.save(path, exif=exif_bytes)
        image.close()

    def read_image_metadata(self, image_uuid: UUID) -> ImageData:
        """ Read the image metadata stubs to form an Image data blob """
        image_data = ImageData()

        path = self.get_image_path(image_uuid)
        image = Image.open(path)

        # noinspection PyProtectedMember
        exif_data = image.getexif()

        if not exif_data:
            return image_data

        if EXIF_TAG_ORIGINAL_RAW_FILE_NAME in exif_data:
            image_data.file_name = exif_data[EXIF_TAG_ORIGINAL_RAW_FILE_NAME]
            image_data.file_name = image_data.file_name.decode("UTF-8")

        image.close()

        return image_data

    def delete_image(self, image_uuid: UUID) -> None:
        if not os.path.exists(self.get_image_path(image_uuid)):
            raise FileNotFoundError("Missing Image")
        os.remove(self.get_image_path(image_uuid))

    def import_image(self, image_path: Path, image_name = "") -> (UUID, ImageData):
        """ Import an image from a remote location into the bank """
        try:
            # Make UUID for image
            image_uuid = generate_uuid()

            # Get image new path
            new_image_path = self.get_image_path(image_uuid)

            # Extract Image name from image
            if not image_name:
                image_name, _ = os.path.splitext(os.path.basename(image_path))

            # Build image data blob
            image_data = ImageData(file_name=image_name)

            # Copy image file to the bank
            shutil.copy(image_path, new_image_path)

            # Write copied image's metadata
            self.write_image_metadata(image_uuid, image_data)

            # Append this image to the bank index
            # self.images[image_uuid] = image_data

            # return the uuid and image data blob of this new image
            return image_uuid, image_data
        except Exception as e:
            print(f"IMAGE_BANK IMPORT - Error importing image: {str(e)}")

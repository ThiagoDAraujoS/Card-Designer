import os
import shutil
from os import path
from image_folder import ImageFolder
from data import Card
from registry import Registry


class CardEditor:
    def __init__(self, image_folder: ImageFolder, bank_manager: BankRegistry, main_path):
        self.MAIN_PATH: str = main_path
        self.image_folder: ImageFolder = image_folder
        self.bank_manager: Registry = bank_manager
        self.inspected_card: Card | None = None

    def create(self, card_name: str, image_file_name: str) -> None:

        image_file_path = os.path.join(self.image_folder.path, image_file_name)
        if not os.path.exists(image_file_path) or not os.path.isfile(image_file_path):
            print(f"Image file '{image_file_name}' not found in the image folder.")
            return

        # Copy the image file to the image bank with the new name
        new_image_file_name = f"{card_name}.jpg"
        destination_path = os.path.join(self.bank_manager.inspected_image_bank_path, new_image_file_name)
        if os.path.exists(destination_path):
            print(f"Card '{card_name}' already exists in the image bank as '{new_image_file_name}'.")
            return

        try:
            shutil.copy(image_file_path, destination_path)
            new_card = Card(image=new_image_file_name)
            print(f"Added card '{card_name}' to the image bank as '{new_image_file_name}'.")
        except Exception as e:
            print(f"An error occurred while adding the card to the image bank: {e}")

        self.bank_manager.inspected_bank.add_card()


    def create(self, card_name: str) -> None:

        image_file_path = os.path.join(self.image_folder.path, image_file_name)
        if not os.path.exists(image_file_path) or not os.path.isfile(image_file_path):
            print(f"Image file '{image_file_name}' not found in the image folder.")
            return

        # Copy the image file to the image bank with the new name
        new_image_file_name = f"{card_name}.jpg"
        destination_path = os.path.join(self.bank_manager.inspected_image_bank_path, new_image_file_name)
        if os.path.exists(destination_path):
            print(f"Card '{card_name}' already exists in the image bank as '{new_image_file_name}'.")
            return

        try:
            shutil.copy(image_file_path, destination_path)
            new_card = Card(image=new_image_file_name)
            print(f"Added card '{card_name}' to the image bank as '{new_image_file_name}'.")
        except Exception as e:
            print(f"An error occurred while adding the card to the image bank: {e}")

        self.bank_manager.inspected_bank.add_card()
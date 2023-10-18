import os
import shutil
from os import path
from typing import List
from data import Card, Bank


class BankManager:
    """ This class is designed to facilitate the management of bank folders.
        Banks, in this context, represent directories containing card images and their associated metafiles.
    """

    def __init__(self, main_path):
        self.MAIN_PATH: str = main_path
        self.existing_bank_names: List[str] = []
        self.inspected_image_bank_path: str = ""
        self.inspected_data_bank_path: str = ""
        self.inspected_bank: Bank | None = None

    def clear(self):
        """ Clear the inspected bank """
        self.inspected_bank = None
        self.inspected_data_bank_path = ""
        self.inspected_image_bank_path = ""

    def save(self):
        """ Save the inspected bank to file """
        try:
            with open(self.inspected_data_bank_path, 'w') as data_file:
                json_string = self.inspected_bank.to_json(indent=2)
                data_file.write(json_string)
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")

    def inspect(self, bank_name: str) -> None:
        """Set the card data bank file paths based on the selected bank_name."""
        bank_folder_path = path.join(self.MAIN_PATH, bank_name)

        # Construct paths for image and data banks
        self.inspected_image_bank_path = path.join(bank_folder_path, "images")
        self.inspected_data_bank_path = path.join(bank_folder_path, "data.json")

        if not path.exists(self.inspected_image_bank_path) or not path.exists(self.inspected_data_bank_path):
            print(f"Bank {bank_name} not found or incomplete.")
            return

        try:
            with open(self.inspected_data_bank_path, 'r') as data_file:
                json_string = data_file.read()
                self.inspected_bank = Bank.from_json(json_string)
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")
            return

        print(f"Selected bank: {bank_name}")

    def load(self) -> None:
        """Read all folders inside self.tool_path and build self.existing_bank_names."""
        if not (path.exists(self.MAIN_PATH) and path.isdir(self.MAIN_PATH)):
            print(f"Tool path {self.MAIN_PATH} does not exist or is not a directory.")
            return
        self.existing_bank_names = [name for name in os.listdir(self.MAIN_PATH) if path.isdir(path.join(self.MAIN_PATH, name))]

    def create(self, name: str) -> None:
        """Create a new card bank with the given name."""
        bank_folder_path = path.join(self.MAIN_PATH, name)

        if path.exists(bank_folder_path):
            print(f"Bank {name} already exists.")
            return

        # Create the bank folder
        os.mkdir(bank_folder_path)

        # Create an empty data.json file
        data_file_path = path.join(bank_folder_path, "data.json")
        with open(data_file_path, 'w') as data_file:
            data_file.write(Bank().to_json(indent=2))

        # Create an empty 'images' folder
        images_folder_path = path.join(bank_folder_path, "images")
        os.mkdir(images_folder_path)

        self.load()
        print(f"Created bank: {name}")

    def copy(self, source_bank_name: str, new_bank_name: str) -> None:
        """Copy an existing card bank and change its name."""
        source_folder_path = path.join(self.MAIN_PATH, source_bank_name)
        destination_folder_path = path.join(self.MAIN_PATH, new_bank_name)

        if not path.exists(source_folder_path) or path.exists(destination_folder_path):
            print("Source bank does not exist or the destination bank already exists.")
            return

        try:
            # Copy the existing bank to create a new one with a different name
            shutil.copytree(source_folder_path, destination_folder_path)
            print(f"Successfully copied bank '{source_bank_name}' to '{new_bank_name}'")
        except Exception as e:
            print(f"An error occurred while copying the bank: {e}")

    def delete(self, bank_name: str) -> None:
        """Delete an existing card bank."""
        bank_folder_path = path.join(self.MAIN_PATH, bank_name)

        if not path.exists(bank_folder_path) or not path.isdir(bank_folder_path):
            print(f"Bank '{bank_name}' does not exist or is not a directory.")
            return

        try:
            # Delete the bank folder and its contents
            shutil.rmtree(bank_folder_path)
            print(f"Successfully deleted bank '{bank_name}'")
        except Exception as e:
            print(f"An error occurred while deleting the bank: {e}")

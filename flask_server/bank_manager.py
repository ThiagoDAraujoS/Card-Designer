import os
import shutil
from os import path
import json
from typing import List


class BankManager:
    """ This class is designed to facilitate the management of bank folders.
        Banks, in this context, represent directories containing card images and their associated metafiles.
    """

    def __init__(self):
        self.tool_path: str = ""
        self.existing_bank_names: List[str] = []
        self.inspected_image_bank_path: str = ""
        self.inspected_data_bank_path: str = ""

    def inspect(self, bank_name: str) -> None:
        """Set the card data bank file paths based on the selected bank_name."""
        bank_folder_path = path.join(self.tool_path, bank_name)

        # Construct paths for image and data banks
        self.inspected_image_bank_path = path.join(bank_folder_path, "images")
        self.inspected_data_bank_path = path.join(bank_folder_path, "data.json")

        # Check if the image and data bank paths exist
        if path.exists(self.inspected_image_bank_path) and path.exists(self.inspected_data_bank_path):
            print(f"Selected bank: {bank_name}")
        else:
            print(f"Bank {bank_name} not found or incomplete.")

    def load(self) -> None:
        """Read all folders inside self.tool_path and build self.existing_bank_names."""
        if not (path.exists(self.tool_path) and path.isdir(self.tool_path)):
            print(f"Tool path {self.tool_path} does not exist or is not a directory.")
            return
        self.existing_bank_names = [name for name in os.listdir(self.tool_path) if path.isdir(path.join(self.tool_path, name))]

    def create(self, name: str) -> None:
        """Create a new card bank with the given name."""
        bank_folder_path = path.join(self.tool_path, name)

        if path.exists(bank_folder_path):
            print(f"Bank {name} already exists.")
            return

        # Create the bank folder
        os.mkdir(bank_folder_path)

        # Create an empty data.json file
        data_file_path = path.join(bank_folder_path, "data.json")
        with open(data_file_path, 'w') as data_file:
            json.dump({}, data_file)

        # Create an empty 'images' folder
        images_folder_path = path.join(bank_folder_path, "images")
        os.mkdir(images_folder_path)

        self.load()
        print(f"Created bank: {name}")

    def copy(self, source_bank_name: str, new_bank_name: str) -> None:
        """Copy an existing card bank and change its name."""
        source_folder_path = path.join(self.tool_path, source_bank_name)
        destination_folder_path = path.join(self.tool_path, new_bank_name)

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
        bank_folder_path = path.join(self.tool_path, bank_name)

        if not path.exists(bank_folder_path) or not path.isdir(bank_folder_path):
            print(f"Bank '{bank_name}' does not exist or is not a directory.")
            return

        try:
            # Delete the bank folder and its contents
            shutil.rmtree(bank_folder_path)
            print(f"Successfully deleted bank '{bank_name}'")
        except Exception as e:
            print(f"An error occurred while deleting the bank: {e}")

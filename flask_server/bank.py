from dataclasses_json import dataclass_json
from dataclasses import dataclass, field
import os
from os import path
import shutil
from typing import Set
from data import Card


@dataclass_json
@dataclass
class Data:
    """ Container for a set of defined cards """
    cards: Set[Card] = field(default_factory=list)


class Bank:
    """ Card Bank representation, this class can be serialized and deserialized """

    MAIN_PATH = ""

    def __init__(self):
        self.bank_path = ""
        """ The folder where this bank is located """

        self.data_path = ""
        """ Path to the data.json file """

        self.images_path = ""
        """ Path to the images folder """

        self.data: Data = Data()
        """ Serialized Card Bank """

    @staticmethod
    def create(bank_name: str) -> None:
        """ Create a new card bank with the given name. """
        self = Bank()

        bank_folder_path = path.join(Bank.MAIN_PATH, bank_name)

        if path.exists(bank_folder_path):
            print(f"Bank {bank_name} already exists.")
            return

        # Create the bank folder
        os.mkdir(bank_folder_path)

        # Create an empty data.json file
        data_file_path = path.join(bank_folder_path, "data.json")
        with open(data_file_path, 'w') as data_file:
            data_file.write(self.to_json(indent=2))

        # Create an empty 'images' folder
        images_folder_path = path.join(bank_folder_path, "images")
        os.mkdir(images_folder_path)

        print(f"Created bank: {bank_name}")

    @staticmethod
    def copy(source_name: str, new_name: str):
        """ Copy an existing card bank and change its name. """
        source_folder_path = path.join(Bank.MAIN_PATH, source_name)
        destination_folder_path = path.join(Bank.MAIN_PATH, new_name)

        if not path.exists(source_folder_path) or path.exists(destination_folder_path):
            print("Source bank does not exist or the destination bank already exists.")
            return

        try:
            shutil.copytree(source_folder_path, destination_folder_path)
            print(f"Successfully copied bank '{source_name}' to '{new_name}'")
        except Exception as e:
            print(f"An error occurred while copying the bank: {e}")

        return Bank.load(new_name)

    @staticmethod
    def load(bank_name):
        """ Form a Bank object out of a data file """
        self = Bank()
        self.bank_path = path.join(Bank.MAIN_PATH, bank_name)
        self.data_path = path.join(self.bank_path, "data.json")
        self.images_path = path.join(self.bank_path, "images")

        if not path.exists(self.images_path) or not path.exists(self.data_path):
            print(f"Bank {bank_name} not found or incomplete.")
            return

        try:
            with open(self.data_path, 'r') as data_file:
                json_string = data_file.read()
                self.data = Data.from_json(json_string)
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")
            return

        print(f"Selected bank: {bank_name}")
        return self

    def save(self):
        """ Save the inspected bank to file """
        try:
            with open(self.data_path, 'w') as data_file:
                json_string = self.data.to_json(indent=2)
                data_file.write(json_string)
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")

    def exists(self):
        """ Check if all required folders and files exist.

        Returns:
            bool: True if all required components exist, False otherwise.
        """
        # Check if the bank_path directory exists
        if not os.path.exists(self.bank_path):
            return False

        # Check if the data_path file exists
        if not os.path.exists(self.data_path):
            return False

        # Check if the images_path directory exists
        if not os.path.exists(self.images_path):
            return False

        return True

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
    """ Data class for managing a collection of cards. """
    cards: Set[Card] = field(default_factory=list)
    """ A set of cards contained in the data. """


class Bank:
    """ Bank class for managing card banks and their file representation. """

    MAIN_PATH = ""
    """ The main path where banks are located. """

    def __init__(self, name):
        """ Initializes a Bank object with the given name. """

        self.name = name
        """ The name of the bank. """

        self.bank_path = path.join(Bank.MAIN_PATH, self.name)
        """ The path to the bank folder. """

        self.data_path = path.join(self.bank_path, "data.json")
        """ The path to the data.json file. """

        self.images_path = path.join(self.bank_path, "images")
        """ The path to the images folder. """

        self.data: Data = Data()
        """ Serialized card bank data. """

    @staticmethod
    def is_legal(name) -> bool:
        """ Checks if the bank folder and required files exist. """
        bank_path = path.join(Bank.MAIN_PATH, name)
        data_path = path.join(bank_path, "data.json")
        images_path = path.join(bank_path, "images")

        if not path.exists(bank_path):
            print(f"Bank {bank_path} folder does not exist.")
            return False

        if not path.exists(images_path):
            print(f"Bank {images_path} folder does not exist.")
            return False

        if not path.exists(data_path):
            print(f"Bank {data_path} file does not exist.")
            return False

        return True

    @staticmethod
    def _is_empty(name) -> bool:
        """ Checks if the bank folder and required files do not exist. """
        bank_path = path.join(Bank.MAIN_PATH, name)
        data_path = path.join(bank_path, "data.json")
        images_path = path.join(bank_path, "images")

        if path.exists(bank_path):
            print(f"Bank {bank_path} folder already exists.")
            return False

        if path.exists(images_path):
            print(f"Bank {images_path} folder already exists.")
            return False

        if path.exists(data_path):
            print(f"Bank {data_path} file already exists.")
            return False

        return True

    @staticmethod
    def create(bank_name: str):
        """ Creates a new bank with the given name. """
        self = Bank(bank_name)

        if not Bank._is_empty(bank_name): return

        os.mkdir(self.bank_path)
        os.mkdir(self.images_path)
        with open(self.data_path, 'w') as data_file:
            data_file.write(self.data.to_json(indent=2))

        print(f"Created bank: {bank_name}")
        return self

    @staticmethod
    def copy(source_name: str, new_name: str):
        """ Copies an existing bank to a new bank with a different name. """
        source_folder_path = path.join(Bank.MAIN_PATH, source_name)
        destination_folder_path = path.join(Bank.MAIN_PATH, new_name)

        if not Bank.is_legal(source_name):
            print("Source bank does not exist.")
            return

        if not Bank._is_empty(new_name):
            print("The destination bank already exists.")
            return

        try:
            shutil.copytree(source_folder_path, destination_folder_path)
            print(f"Successfully copied bank '{source_name}' to '{new_name}'")

        except Exception as e:
            print(f"An error occurred while copying the bank: {e}")

        return Bank.load(new_name)

    @staticmethod
    def load(bank_name):
        """ Loads the data of an existing bank. """
        self = Bank(bank_name)
        if not Bank.is_legal(bank_name): return
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
        """ Saves the bank data to the data.json file. """
        if not Bank.is_legal(self.name): return
        try:
            with open(self.data_path, 'w') as data_file:
                json_string = self.data.to_json(indent=2)
                data_file.write(json_string)
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")

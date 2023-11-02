import os
from abc import abstractmethod
from os import path
import shutil
from dataclasses_json import dataclass_json
from . import PathString, JsonString


class Bank:
    """ Bank class for managing card banks and their file representation. """
    META_FILE_NAME: str = "index.json"
    CACHE_FOLDER_NAME: str = "files"

    def __init__(self, name: str, main_path: PathString):
        """ Initializes a Bank object with the given name. """

        self.name: str = name
        """ The name of the bank. """

        self.path: PathString = PathString(path.join(main_path, self.name))
        """ The path to the bank folder. """

        self.meta_path: PathString = PathString(path.join(self.path, self.__class__.META_FILE_NAME))
        """ The path to the index.json file. """

        self.cache_path: PathString = PathString(path.join(self.path, self.__class__.CACHE_FOLDER_NAME))
        """ The path to the images folder. """

        self.data = self._init_data()
        """ Serialized card bank data. """

    @abstractmethod
    def _init_data(self) -> dataclass_json:
        return dataclass_json()

    @abstractmethod
    def _data_from_json(self, json_string: JsonString) -> dataclass_json:
        return dataclass_json()

    def is_legal(self) -> bool:
        """ Return if the folder structure of this bank is legal """
        return all((path.exists(self.path), path.exists(self.cache_path), path.exists(self.meta_path)))

    def is_empty(self) -> bool:
        """ Checks if the bank folder and required files do not exist. """
        return not any((path.exists(self.path), path.exists(self.cache_path), path.exists(self.meta_path)))

    def build(self) -> None:
        """ Build this bank folder structure and base files """
        os.mkdir(self.path)
        os.mkdir(self.cache_path)
        with open(self.meta_path, 'w') as data_file:
            data_file.write(self.data.to_json(indent=2))

    @classmethod
    def create(cls, bank_name: str, main_path: PathString):
        """ Creates a new bank with the given name. """
        instance = cls(bank_name, main_path)

        if not instance.is_empty():
            raise Exception("Bank already exists")

        instance.build()

        print(f"{bank_name} bank was created")
        return instance

    def copy(self, new_name: str, main_path: PathString):
        """ Copies an existing bank to a new bank with a different name. """
        instance = self.__class__(new_name, main_path)

        if not self.is_legal():
            raise Exception("Source bank does not exist")

        if not instance.is_empty():
            raise Exception("The destination bank already exists")

        try:
            shutil.copytree(self.path, instance.path)
            print(f"Successfully copied bank '{self.name}' to '{instance.name}'")
        except Exception as e:
            raise Exception(f"An error occurred while copying the bank: {e}")
        instance.load()
        return instance

    def load(self):
        """ Loads the data of an existing bank. """
        if not self.is_legal():
            raise Exception("Invalid bank structure")
        try:
            with open(self.meta_path, 'r') as data_file:
                json_string = JsonString(data_file.read())
                self.data = self._data_from_json(json_string)

        except Exception as e:
            raise Exception(f"An error occurred while loading the data: {e}")

        print(f"Selected bank: {self.name}")

    def clear(self) -> None:
        """ Erase all bank's data """
        self.data = self._init_data()

    def save(self) -> None:
        """ Saves the bank data to the data.json file. """
        if not self.is_legal():
            raise Exception("Invalid bank structure")
        try:
            with open(self.meta_path, 'w') as data_file:
                json_string = self.data.to_json(indent=2)
                data_file.write(json_string)
        except Exception as e:
            raise Exception(f"An error occurred while saving the data: {e}")

    def delete(self) -> None:
        """ Delete this bank's files """
        shutil.rmtree(self.path)
        self.data = self._init_data()

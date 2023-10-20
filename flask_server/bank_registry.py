import os
from os import path
import shutil
from typing import Set
from bank import Bank


class BankRegistry:
    MAIN_PATH = ""
    """ MAIN_PATH (str): The main path where banks are located. """

    def __init__(self):
        """ Initializes a BankRegistry object with the main path for managing banks. """
        Bank.MAIN_PATH = BankRegistry.MAIN_PATH

        self.registry: Set[str] = set()
        """ A set to store bank names in the registry. """

    @staticmethod
    def ensure_bank_exists(func):
        """ Decorator to ensure that a bank exists before executing a method. """
        def inner(self, bank_name: str, *args, **kwargs):
            result = True
            if bank_name not in self.registry:
                print(f"{bank_name} does not exist in registry")
                result = False

            if not Bank.is_legal(bank_name):
                result = False

            if result:
                return func(self, bank_name, *args, **kwargs)

        return inner

    @staticmethod
    def reload_registry(func):
        """ Decorator to reload the bank registry after executing a method. """
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.initialize()
        return inner

    def initialize(self) -> None:
        """ This method scans the main path for bank folders and adds their names to the registry set. """
        self.registry = set()
        for name in os.listdir(Bank.MAIN_PATH):
            if path.isdir(path.join(Bank.MAIN_PATH, name)):
                self.registry.add(name)

    @ensure_bank_exists
    def inspect(self, bank_name: str) -> Bank | None:
        """ Inspects a bank and returns the corresponding Bank object. """
        return Bank.load(bank_name)

    @ensure_bank_exists
    @reload_registry
    def delete(self, bank_name: str) -> None:
        """ Deletes a bank. """
        bank_folder_path = path.join(BankRegistry.MAIN_PATH, bank_name)
        try:
            shutil.rmtree(bank_folder_path)
            print(f"Successfully deleted bank '{bank_name}'")
        except Exception as e:
            print(f"An error occurred while deleting the bank: {e}")

    @ensure_bank_exists
    @reload_registry
    def copy(self, bank_name: str, new_bank_name: str) -> Bank | None:
        """ Copies an existing bank to a new bank with a different name. """
        return Bank.copy(bank_name, new_bank_name)

    @reload_registry
    def create(self, bank_name: str) -> Bank | None:
        """ Creates a new bank with the given name. """
        return Bank.create(bank_name)

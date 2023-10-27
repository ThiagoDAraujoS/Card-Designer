import os
from os import path
import shutil
from typing import Set

from flask_server.app.card_bank import CardBank
from flask_server.app.image_bank import ImageBank
from flask_server.app.bank import Bank


class BankRegistry:
    MAIN_PATH = ""
    """ MAIN_PATH (str): The main path where banks are located. """
    IMAGE_BANK_NAME = "images"
    REGISTRY_FOLDER_NAME = "banks"

    def __init__(self):
        """ Initializes a BankRegistry object with the main path for managing banks. """
        self.registry_path = path.join(BankRegistry.MAIN_PATH, BankRegistry.REGISTRY_FOLDER_NAME)
        if not path.exists(self.registry_path):
            os.mkdir(self.registry_path)
        Bank.MAIN_PATH = self.registry_path
        self.image_bank: ImageBank | None = None
        self.registry: Set[str] = set()
        self.registry_path = ""
        self.initialize()

    def initialize(self):
        self.image_bank = ImageBank(BankRegistry.IMAGE_BANK_NAME)
        if self.image_bank.is_empty():
            self.image_bank.build()
        elif not self.image_bank.is_legal():
            raise Exception("Image bank is not legal")
        else:
            self.image_bank.load()

        self.registry = set()
        self.registry_path = path.join(BankRegistry.MAIN_PATH, BankRegistry.REGISTRY_FOLDER_NAME)

        for folder_name in os.listdir(self.registry_path):
            if path.isdir(path.join(Bank.MAIN_PATH, folder_name)):
                new_bank = CardBank(folder_name)
                if new_bank.is_legal():
                    self.registry.add(folder_name)
                    print(f"{new_bank} loaded successfully")

    @staticmethod
    def ensure_bank_exists(func):
        """ This decorator uses the first argument of a method as a string
            Then builds a bank object out of it, and verify if this bank is legal.
            If it's not this decorator will throw an error.
            If it is, this decorator will invoke the decorated method
            but using the bank object as first argument instead of its str name"""

        def inner(self, bank_name: str, *args, **kwargs):
            if bank_name not in self.registry:
                raise Exception("Bank not found in the registry")

            new_bank = CardBank(bank_name)
            if not new_bank.is_legal():
                raise Exception("Invalid bank structure")

            func(self, new_bank, *args, **kwargs)

        return inner

    @staticmethod
    def reload_registry(func):
        """ Decorator to reload the bank registry after executing a method. """
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.initialize()
        return inner

    @ensure_bank_exists
    def inspect(self, bank: str | CardBank) -> CardBank:
        """ Inspects a bank and returns the corresponding Bank object. """
        bank.load()
        return bank

    @ensure_bank_exists
    @reload_registry
    def delete(self, bank: str | CardBank) -> None:
        """ Deletes a bank. """
        try:
            shutil.rmtree(bank.path)
            print(f"Successfully deleted bank '{bank}'")
        except Exception as e:
            print(f"An error occurred while deleting the bank: {e}")

    @ensure_bank_exists
    @reload_registry
    def copy(self, bank: str | CardBank, new_bank_name: str) -> CardBank:
        """ Copies an existing bank to a new bank with a different name. """
        return bank.copy(new_bank_name)

    @reload_registry
    def create(self, bank_name: str) -> CardBank:
        """ Creates a new bank with the given name. """
        new_bank = CardBank.create(bank_name)
        self.registry.add(new_bank.name)
        return new_bank

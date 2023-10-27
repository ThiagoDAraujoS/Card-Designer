import os
from os import path
import shutil
from typing import Set

from flask_server.app.card_bank import CardBank
from flask_server.app.image_bank import ImageBank
from flask_server.app.bank import Bank


class Registry:
    MAIN_PATH = ""
    """ The main path where banks are located. """

    IMAGE_BANK_NAME = "images"
    REGISTRY_FOLDER_NAME = "banks"

    def __init__(self):
        """ Initializes a BankRegistry object with the main path for managing banks. """
        self.path = path.join(Registry.MAIN_PATH, Registry.REGISTRY_FOLDER_NAME)
        if not path.exists(self.path):
            os.mkdir(self.path)
        Bank.MAIN_PATH = self.path
        self.image_bank: ImageBank | None = None
        self.card_bank_names: Set[str] = set()
        self.inspected_bank: CardBank | None = None
        self.load_registry()

    def load_registry(self):
        self.image_bank = ImageBank(Registry.IMAGE_BANK_NAME)

        if self.image_bank.is_empty():
            self.image_bank.build()
        elif not self.image_bank.is_legal():
            raise Exception("Image bank is not legal")
        else:
            self.image_bank.load()

        self.card_bank_names = set()
        self.path = path.join(Registry.MAIN_PATH, Registry.REGISTRY_FOLDER_NAME)

        for folder_name in os.listdir(self.path):
            if path.isdir(path.join(Bank.MAIN_PATH, folder_name)):
                new_bank = CardBank(folder_name)
                if new_bank.is_legal():
                    self.card_bank_names.add(folder_name)
                    print(f"{new_bank} loaded successfully")

    @staticmethod
    def ensure_bank_is_legal(func):
        """ This decorator uses the first argument of a method as a string
            Then builds a bank object out of it, and verify if this bank is legal.
            If it's not this decorator will throw an error.
            If it is, this decorator will invoke the decorated method
            but using the bank object as first argument instead of its str name"""

        def inner(self, bank_name: str, *args, **kwargs):
            if bank_name not in self.card_bank_names:
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
            self.load_registry()
        return inner

    @ensure_bank_is_legal
    def load_bank(self, bank: str | CardBank) -> CardBank:
        """ Inspects a bank and returns the corresponding Bank object. """
        if self.inspected_bank:
            self.inspected_bank.unload()
        self.inspected_bank = bank
        bank.load()
        return bank

    @ensure_bank_is_legal
    @reload_registry
    def delete_bank(self, bank: str | CardBank) -> None:
        """ Deletes a bank. """
        try:
            shutil.rmtree(bank.path)
            print(f"Successfully deleted bank '{bank}'")
        except Exception as e:
            print(f"An error occurred while deleting the bank: {e}")

    @ensure_bank_is_legal
    @reload_registry
    def copy_bank(self, bank: str | CardBank, new_bank_name: str) -> CardBank:
        """ Copies an existing bank to a new bank with a different name. """
        return bank.copy(new_bank_name)

    @reload_registry
    def create_bank(self, bank_name: str) -> CardBank:
        """ Creates a new bank with the given name. """
        new_bank = CardBank.create(bank_name)
        self.card_bank_names.add(new_bank.name)
        return new_bank

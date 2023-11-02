import os
from os import path
import shutil
from typing import Set

from flask_server.app.card_bank import CardBank
from flask_server.app.image_bank import ImageBank
from . import PathString


class Registry:
    IMAGE_BANK_NAME = "images"
    REGISTRY_FOLDER_NAME = "banks"

    def __init__(self, main_path: PathString):
        """ Initializes a BankRegistry object with the main path for managing banks. """
        self.main_path: PathString = main_path
        """ This registry folder path """

        self.card_bank_path: PathString = PathString(path.join(self.main_path, Registry.REGISTRY_FOLDER_NAME))
        """ The path within the registry to where card banks are stored """

        self.image_bank: ImageBank | None = None
        """ Reference to the image bank object that oversee the images """

        self.card_bank_names: Set[str] = set()
        """ Reference to all card banks names stored in the card bank folder """

        self.inspected_bank: CardBank | None = None
        """ Reference to an inspected card bank, this bank will have all its cards loaded in memory """

    def build_registry(self) -> None:
        """ This method assign the registry path variables and build all missing structural folders """
        # Rebuild the image bank primitive
        self.image_bank = ImageBank(Registry.IMAGE_BANK_NAME, self.main_path)

        # Verify if the image bank folder exists, if it does not, make it, and if it does,
        # ensure it's a folder structure suitable to host a bank primitive
        if self.image_bank.is_empty():
            self.image_bank.build()
        elif not self.image_bank.is_legal():
            raise Exception("Image bank is not legal")
        else:
            self.image_bank.load()

        # Reconstruct the card bank folder path and initialize an empty card bank set to hold each bank
        self.card_bank_path = PathString(path.join(self.main_path, Registry.REGISTRY_FOLDER_NAME))
        self.card_bank_names = set()

        # If the card bank folder exists, peer through it in order to collect all stashed banks,
        if path.exists(self.card_bank_path):
            for folder_name in os.listdir(self.card_bank_path):
                if path.isdir(path.join(self.card_bank_path, folder_name)):
                    new_bank = CardBank(folder_name, self.card_bank_path)
                    if new_bank.is_legal():
                        self.card_bank_names.add(folder_name)
                        print(f"{new_bank} loaded successfully")

        # If not create a new card banks folder
        else:
            os.mkdir(self.card_bank_path)

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

            new_bank = CardBank(bank_name, self.card_bank_path)
            if not new_bank.is_legal():
                raise Exception("Invalid bank structure")

            return func(self, new_bank, *args, **kwargs)

        return inner

    @staticmethod
    def reload_registry(func):
        """ Decorator to reload the bank registry after executing a method. """
        def inner(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.build_registry()
            return result
        return inner

    @ensure_bank_is_legal
    def load_bank(self, bank: str | CardBank) -> CardBank:
        """ Inspects a bank and returns the corresponding Bank object. """
        if self.inspected_bank:
            self.inspected_bank.clear()
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
        return bank.copy(new_bank_name, self.card_bank_path)

    @reload_registry
    def create_bank(self, bank_name: str) -> CardBank:
        """ Creates a new bank with the given name. """
        new_bank = CardBank.create(bank_name, self.card_bank_path)
        self.card_bank_names.add(new_bank.name)
        return new_bank

import os
from os import path
import shutil
from typing import List
from bank import Bank


class BankManager:
    """ This class is designed to facilitate the management of bank folders.
        Banks, in this context, represent directories containing card images and their associated metafiles. """

    def __init__(self, main_path):
        self.MAIN_PATH: str = main_path
        Bank.MAIN_PATH = main_path
        self.existing_bank_names: List[str] = []
        self.inspected_bank: Bank | None = None

    def clear(self) -> None:
        """ Clear the inspected bank """
        self.inspected_bank = None

    def inspect(self, bank_name: str) -> None:
        """ Set the card data bank file paths based on the selected bank_name. """
        self.inspected_bank = Bank.load(bank_name)

    def load(self) -> None:
        """ Read all folders inside self.tool_path and build self.existing_bank_names. """
        if not (path.exists(self.MAIN_PATH) and path.isdir(self.MAIN_PATH)):
            print(f"Tool path {self.MAIN_PATH} does not exist or is not a directory.")
            return
        self.existing_bank_names = [name for name in os.listdir(self.MAIN_PATH) if path.isdir(path.join(self.MAIN_PATH, name))]

    def delete(self, bank_name: str) -> None:
        """ Delete an existing card bank. """
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

        if not self.inspected_bank.exists():
            self.clear()

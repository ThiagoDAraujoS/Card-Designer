from unittest import TestCase
import os
import shutil
from flask_server.app.bank import Bank
from flask_server.app.data import Card

class TestBank(TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = 'test_bank_temp_dir'
        os.mkdir(self.temp_dir)
        self.bank_name = 'test_bank'
        self.bank_path = os.path.join(self.temp_dir, self.bank_name)
        self.bank = Bank(self.bank_name, self.temp_dir)

    def tearDown(self):
        # Clean up the temporary directory after the tests
        shutil.rmtree(self.temp_dir)

    def test_create(self):
        # Test the create method
        created_bank = Bank.create(self.bank_name, self.temp_dir)

        # Assert that the created bank is not None and the bank folder exists
        self.assertIsNotNone(created_bank)
        self.assertTrue(os.path.exists(self.bank_path))

    def test_copy(self):
        # Test the copy method
        self.bank.build()
        copied_bank_name = 'copied_bank'
        copied_bank = self.bank.copy(copied_bank_name, self.temp_dir)

        # Assert that the copied bank is not None and the folder exists
        self.assertIsNotNone(copied_bank)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, copied_bank_name)))

    def test_load(self):
        # Test the load method
        self.bank.build()
        self.bank.load()

        # Assert that the bank is loaded successfully
        self.assertTrue(self.bank.is_legal())

    def test_unload(self):
        # Test the unload method
        self.bank.unload()

        # Assert that the bank data is cleared
        self.assertEqual(len(self.bank.data.cards), 0)

    def test_save(self):
        # Test the save method
        self.bank.build()
        card = Card()  # Replace with your actual card class
        self.bank.data.cards.append(card)
        self.bank.save()

        # Assert that the bank data is saved
        self.assertTrue(os.path.exists(self.bank.meta_path))

    def test_delete(self):
        # Test the delete method
        self.bank.build()
        self.bank.delete()

        # Assert that the bank folder is deleted
        self.assertFalse(os.path.exists(self.bank_path))

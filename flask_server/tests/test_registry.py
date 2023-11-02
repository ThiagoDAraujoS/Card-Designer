from unittest import TestCase
from flask_server.app.registry import Registry
from flask_server.app.card_bank import CardBank
from flask_server.app.image_bank import ImageBank
import os
import shutil


class TestBankRegistry(TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = 'test_registry_temp_dir'
        os.mkdir(self.temp_dir)
        self.registry = Registry(self.temp_dir)

    def tearDown(self):
        # Clean up the temporary directory after the tests
        shutil.rmtree(self.temp_dir)

    def test_build_registry_with_existing_image_bank(self):
        # Create an image bank and ensure it's not empty
        image_bank = ImageBank(Registry.IMAGE_BANK_NAME, self.temp_dir)
        image_bank.build()
        self.assertFalse(image_bank.is_empty())

        # Call the build_registry method
        self.registry.build_registry()

        # Assert that the image bank is legal after the operation
        self.assertTrue(image_bank.is_legal())

    def test_build_registry_with_existing_card_banks(self):
        # Create a temporary card bank folder with one card bank
        card_bank_name = 'test_card_bank'
        card_bank_folder_path = os.path.join(self.temp_dir, Registry.REGISTRY_FOLDER_NAME)
        os.mkdir(card_bank_folder_path)
        CardBank.create(card_bank_name, card_bank_folder_path)

        # Call the build_registry method
        self.registry.build_registry()

        # Assert that the card bank folder and name are correctly added
        self.assertIn(card_bank_name, self.registry.card_bank_names)

    def test_build_registry_with_no_existing_card_banks(self):
        # Call the build_registry method when there are no card banks
        self.registry.build_registry()

        # Assert that the card bank folder is created
        card_bank_path = os.path.join(self.temp_dir, Registry.REGISTRY_FOLDER_NAME)
        self.assertTrue(os.path.exists(card_bank_path))

    @staticmethod
    @Registry.ensure_bank_is_legal
    def decorated_method_bank_is_legal(registry, bank):
        # This is a decorated method that expects a CardBank object as the first argument
        return bank

    @staticmethod
    @Registry.reload_registry
    def decorated_method_reload_registry(registry):
        registry.create_bank("test")
        # This is a decorated method that expects no arguments
        return None

    def test_decorator_with_legal_bank(self):
        # Create a legal bank
        legal_bank_name = 'legal_bank'
        self.registry.build_registry()
        self.registry.create_bank(legal_bank_name)

        # Call the decorated method
        result = TestBankRegistry.decorated_method_bank_is_legal(self.registry, legal_bank_name)
        # Assert that the method executed and returned a result (you can customize this)
        self.assertIsNotNone(result)

    def test_decorator_with_illegal_bank(self):
        # Attempt to call the decorated method with an illegal bank
        illegal_bank_name = 'illegal_bank'

        # Since this bank is not legal, the decorated method should raise an exception
        with self.assertRaises(Exception):
            TestBankRegistry.decorated_method_bank_is_legal(illegal_bank_name)

    def test_decorator_reload_registry(self):
        # Call the decorated method before and after, and compare the registry state
        self.registry.build_registry()
        initial_card_bank_names = len(self.registry.card_bank_names)
        # Call the decorated method
        TestBankRegistry.decorated_method_reload_registry(self.registry)

        # Check if the card bank names have been reloaded
        reloaded_card_bank_names = len(self.registry.card_bank_names)
        self.assertNotEqual(initial_card_bank_names, reloaded_card_bank_names)

    def test_load_bank(self):
        self.registry.build_registry()

        # Create a card bank
        bank_name = 'test_bank'
        self.registry.create_bank(bank_name)

        # Call the load_bank method with the bank name
        loaded_bank = self.registry.load_bank(bank_name)

        # Assert that the loaded bank is not None and has the correct name
        self.assertIsNotNone(loaded_bank)
        self.assertEqual(loaded_bank.name, bank_name)

    def test_delete_bank(self):
        # Create a card bank
        self.registry.build_registry()
        bank_name = 'test_bank'
        self.registry.create_bank(bank_name)
        bank = self.registry.load_bank(bank_name)
        # Call the delete_bank method with the bank name
        self.registry.delete_bank(bank_name)

        # Assert that the bank no longer exists
        self.assertTrue(bank.is_empty())

    def test_copy_bank(self):
        # Create a card bank
        self.registry.build_registry()

        source_bank_name = 'source_bank'
        source_bank = self.registry.create_bank(source_bank_name)

        # Call the copy_bank method to create a new bank
        new_bank_name = 'new_bank'
        copied_bank = self.registry.copy_bank(source_bank_name, new_bank_name)

        # Assert that the copied bank is not None and has the correct name
        self.assertIsNotNone(copied_bank)
        self.assertEqual(copied_bank.name, new_bank_name)

    def test_create_bank(self):
        # Call the create_bank method to create a new bank
        self.registry.build_registry()
        bank_name = 'new_bank'
        created_bank = self.registry.create_bank(bank_name)

        # Assert that the created bank is not None and has the correct name
        self.assertIsNotNone(created_bank)
        self.assertEqual(created_bank.name, bank_name)
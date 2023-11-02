import unittest
from unittest import TestCase
import os
import shutil
from flask_server.app.bank import Bank
from flask_server.app.data import Card
from flask_server.app.image_bank import ImageBank
from PIL import Image


class TestBank(TestCase):
    T = Bank

    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = 'test_bank_temp_dir'
        os.mkdir(self.temp_dir)
        self.bank_name = 'test_bank'
        self.bank_path = os.path.join(self.temp_dir, self.bank_name)
        self.bank = self.__class__.T(self.bank_name, self.temp_dir)

    def tearDown(self):
        # Clean up the temporary directory after the tests
        shutil.rmtree(self.temp_dir)

    def test_create(self):
        # Test the create method
        created_bank = self.__class__.T.create(self.bank_name, self.temp_dir)

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
        self.bank.clear()

        # Assert that the bank data is cleared
        self.assertEqual(len(self.bank.data.cards), 0)

    def test_delete(self):
        # Test the delete method
        self.bank.build()
        self.bank.delete()

        # Assert that the bank folder is deleted
        self.assertFalse(os.path.exists(self.bank_path))


class TestImageBank(TestBank):
    T = ImageBank

    def setUp(self):
        super().setUp()
        # self.bank = ImageBank(self.bank_name, self.temp_dir)

    def tearDown(self):
        super().tearDown()

    def test_import_image(self):
        # Create a sample JPEG image for testing
        image_path = os.path.join(self.temp_dir, "sample.jpg")
        img = Image.new('RGB', (100, 100))
        img.save(image_path)

        # Import the image
        uuid = self.bank.import_image(image_path, "sample_image")
        self.bank.save()

        # Check if the image was imported and the data was updated
        self.assertTrue(os.path.exists(self.bank.meta_path))
        self.assertTrue(os.path.exists(self.bank.get_image_path(uuid)))
        self.assertIn(uuid, self.bank.data.images)
        self.assertEqual(self.bank.data.images[uuid].name, "sample_image")

    def test_delete_image(self):
        # Create a sample JPEG image for testing
        image_path = os.path.join(self.temp_dir, "sample.jpg")
        img = Image.new('RGB', (100, 100))
        img.save(image_path)

        # Import the image
        uuid = self.bank.import_image(image_path, "sample_image")

        # Delete the imported image
        self.bank.delete_image(uuid)

        # Check if the image was deleted and the data was updated
        self.assertFalse(os.path.exists(self.bank.get_image_path(uuid)))
        self.assertNotIn(uuid, self.bank.data.images)

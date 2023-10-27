from unittest import TestCase
import os
import shutil


class TestBank(TestCase):
    TEST_FOLDER = 'test_files'

    @classmethod
    def setUpClass(cls):
        os.mkdir(TestBank.TEST_FOLDER)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TestBank.TEST_FOLDER):
            shutil.rmtree(TestBank.TEST_FOLDER)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_legal(self):
        self.fail()

    def test__is_empty(self):
        self.fail()

    def test_create(self):
        self.fail()

    def test_copy(self):
        self.fail()

    def test_load(self):
        self.fail()

    def test_save(self):
        self.fail()

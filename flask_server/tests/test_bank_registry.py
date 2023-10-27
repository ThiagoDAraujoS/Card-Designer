from unittest import TestCase
from flask_server.app.bank_registry import BankRegistry
import os
import shutil


class TestBankRegistry(TestCase):
    TEST_FOLDER = 'test_files'

    def setUp(self):
        os.mkdir(TestBankRegistry.TEST_FOLDER)

    def tearDown(self):
        if os.path.exists(TestBankRegistry.TEST_FOLDER):
            shutil.rmtree(TestBankRegistry.TEST_FOLDER)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ensure_bank_exists(self):
        self.fail()

    def test_reload_registry(self):
        self.fail()

    def test_initialize(self):
        self.fail()

    def test_inspect(self):
        self.fail()

    def test_delete(self):
        self.fail()

    def test_copy(self):
        self.fail()

    def test_create(self):
        self.fail()

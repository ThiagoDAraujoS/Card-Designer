from flask_server.app.bank_registry import BankRegistry

BankRegistry.MAIN_PATH = "C:\\Users\\Thiago\\Desktop\\Portifolio Projects\\Card Designer\\project"
registry = BankRegistry()

test_bank_name = "test_bank"
registry.create(test_bank_name)
bank = registry.inspect(test_bank_name)

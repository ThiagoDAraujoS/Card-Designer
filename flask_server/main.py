from flask_server.app.registry import Registry

registry = Registry("C:\\Users\\Thiago\\Desktop\\Portifolio Projects\\Card Designer\\project")
registry.build_registry()
test_bank_name = "test_bank"
registry.create_bank(test_bank_name)
bank = registry.load_bank(test_bank_name)

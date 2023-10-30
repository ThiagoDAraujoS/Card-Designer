from flask_server.app.registry import Registry

registry = Registry("C:\\Users\\Thiago\\Desktop\\Portifolio Projects\\Card Designer\\project")
registry.build_registry()
test_bank_name = "test_bank"
if test_bank_name not in registry.card_bank_names:
    registry.create_bank(test_bank_name)
bank = registry.load_bank(test_bank_name)
image_path = "C:\\Users\\Thiago\\Desktop\\Portifolio Projects\\Card Designer\\cards\\500_F_588701540_XO6FLtRvQYfLNxv7Muz6expY7lkSEJpP.jpg"
registry.image_bank.import_image(image_path, "chickens")

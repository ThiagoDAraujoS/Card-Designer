from flask_server.app.bank import Bank


class CardBank(Bank):
    META_FILE_NAME: str = "card_index.json"
    CACHE_FOLDER_NAME: str = "cards"

    def __init__(self, name, main_path):
        super().__init__(name, main_path)
        pass

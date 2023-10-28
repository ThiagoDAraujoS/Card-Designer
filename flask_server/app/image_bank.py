from flask_server.app.bank import Bank


class ImageBank(Bank):
    META_FILE_NAME: str = "image_index.json"
    CACHE_FOLDER_NAME: str = "images"

    def __init__(self, name, main_path):
        super().__init__(name, main_path)
        pass

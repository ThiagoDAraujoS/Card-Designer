import os


class ImageFolder:
    """ A class for managing the image folder used by the tool to create new cards. """

    def __init__(self):
        """ Initialize an ImageFolder instance with an empty folder path. """
        self.path = ""

    def set_image_folder(self, folder_path: str) -> None:
        """ Set the image folder path if it exists. """
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            print(f"Image folder '{folder_path}' does not exist or is not a directory.")
            return

        self.path = folder_path

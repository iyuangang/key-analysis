from ..config import current_config


class Debug:
    def __init__(self):
        self.enabled = current_config["debug"]

    def log(self, *args):
        if self.enabled:
            print("[DEBUG]", *args)


debug = Debug()

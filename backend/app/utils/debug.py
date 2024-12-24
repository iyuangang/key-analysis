from ..config import current_config


class Debug:
    def __init__(self):
        self.enabled = current_config["debug"]

    def log(self, *args):
        if self.enabled:
            print("[DEBUG]", *args)

    def error(self, *args):
        if self.enabled:
            print("[ERROR]", *args)

    def warn(self, *args):
        if self.enabled:
            print("[WARN]", *args)


debug = Debug()

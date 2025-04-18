import logging


class Logger:
    def __init__(self, pillar):
        self.pillar = pillar

    def _log(self, level, message):
        self.pillar._log(level, message)

    def debug(self, message):
        self._log(logging.DEBUG, message)

    def info(self, message):
        self._log(logging.INFO, message)

    def warn(self, message):
        self._log(logging.WARNING, message)

    def error(self, message):
        self._log(logging.ERROR, message)

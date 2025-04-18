from colorama import Fore as f
from datetime import datetime as dt


class Logger:
    def __init__(self, name="zenlogger", tz=None):
        self.name = name
        self.tz = tz

    def get_time(self):
        now = dt.now(self.tz)
        return f"{now.day}.{now.month}.{now.year} / {now.hour}:{now.minute}:{now.second}.{str(now.microsecond)[:3]}"

    def colored_msg(self, level, msg):
        print(f"{f.BLUE+self.name+f.RESET} {self.get_time()} - [{level}]: {msg}")

    def logs(self, msg):
        print(f"{f.BLUE+self.name+f.RESET} {self.get_time()} - {f.LIGHTYELLOW_EX}logs{f.RESET}: {msg}")

    def info(self, msg):
        self.colored_msg(f"{f.LIGHTMAGENTA_EX}INFO{f.RESET}", msg)

    def success(self,msg):
        self.colored_msg(f"{f.LIGHTGREEN_EX}SUCCESS{f.RESET}", msg)

    def warning(self,msg):
        self.colored_msg(f"{f.LIGHTYELLOW_EX}WARNING{f.RESET}", msg)

    def failed(self,msg):
        self.colored_msg(f"{f.LIGHTRED_EX}FAILED{f.RESET}", msg)

    def error(self,msg):
        self.colored_msg(f"{f.LIGHTRED_EX}ERROR{f.RESET}", msg)

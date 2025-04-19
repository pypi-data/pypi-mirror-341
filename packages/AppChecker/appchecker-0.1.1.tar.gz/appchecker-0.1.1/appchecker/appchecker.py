import shutil
from functools import wraps

from halo import Halo


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class AppChecker:
    def __init__(self, checks=None):
        self.checks = []
        self.spinner = Halo(text="Loading", spinner="dots")
        self.success = 0
        self.failure = 0

    def register_check(self, func):
        """Метод для регистрации функции проверки."""
        self.checks.append(func)
        return func

    async def run_checks(self):
        self.display_message(self.on_center("check starts"))
        print(f"collected {len(self.checks)} items")
        print()
        for check in self.checks:
            result = False
            name = check.__name__

            print(f"Starting {name}...")
            result = await self.load_with_halo(check)

            if result is True:
                self.spinner.succeed(f"[SUCCESS] {name}")
                self.success += 1
            else:
                self.spinner.fail(f"[FAILURE] {name}")
                self.failure += 1

        self.display_results()

    async def load_with_halo(self, check_func):
        """Функция для отображения анимированного лоадера с использованием Halo во время выполнения проверки."""
        with Halo(text="Loading", spinner="dots"):
            result = await check_func()
        return result

    def display_results(self):
        message = f"{self.success} [success]"
        message = self.set_color(self.on_center(message), bcolors.OKGREEN)
        if self.failure:
            message = f"{self.failure} [failure]"
            message = self.set_color(self.on_center(message), bcolors.FAIL)
            self.display_message(message, bcolors.FAIL)
        else:
            self.display_message(message, bcolors.OKGREEN)
        if not self.failure:
            self.display_startup_message("All checks success.")
        elif self.failure == len(self.checks):
            self.display_startup_message("All checks failed.")
        else:
            self.display_startup_message("Some checks failed.")

    def display_startup_message(self, message):
        print(message)

    def set_color(self, message, color=None):
        if color:
            return f"{color}{message}{color}"
        return f"{message}"

    def on_center(self, message):
        terminal_width = shutil.get_terminal_size().columns
        return message.center(terminal_width)

    def display_message(self, message, color=None):
        terminal_width = shutil.get_terminal_size().columns
        dashes = "-" * terminal_width

        print(self.set_color(dashes, color))
        print(f"{message}")
        print(self.set_color(dashes, color))

    def check_health(self, func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                print()
                print(e)
                return False

        self.register_check(wrapper)
        return wrapper

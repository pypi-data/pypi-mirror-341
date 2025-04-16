# textura/textura.py
import builtins
import re

# ANSI Style Classes
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    INVERT = "\033[7m"
    STRIKETHROUGH = "\033[9m"

    @staticmethod
    def get_all():
        return {k: v for k, v in Style.__dict__.items() if not k.startswith("_") and isinstance(v, str)}

class Fore:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[39m"

    # Bright versions
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    @staticmethod
    def get_all():
        return {k: v for k, v in Fore.__dict__.items() if not k.startswith("_") and isinstance(v, str)}

class Back:
    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"
    RESET = "\033[49m"

    # Bright versions
    BRIGHT_BLACK = "\033[100m"
    BRIGHT_RED = "\033[101m"
    BRIGHT_GREEN = "\033[102m"
    BRIGHT_YELLOW = "\033[103m"
    BRIGHT_BLUE = "\033[104m"
    BRIGHT_MAGENTA = "\033[105m"
    BRIGHT_CYAN = "\033[106m"
    BRIGHT_WHITE = "\033[107m"

    @staticmethod
    def get_all():
        return {k: v for k, v in Back.__dict__.items() if not k.startswith("_") and isinstance(v, str)}

# Custom Exception
class PrintError(Exception):
    pass

# Internal config
_config = {
    "resetend": True,
    "strict": True,
}

# Patch the built-in print function (only in strict mode)
_original_print = builtins.print
def _strict_print(*args, **kwargs):
    text = " ".join(str(arg) for arg in args)
    if re.search(r"\{(Fore|Back|Style)\.[A-Z_]+\}", text):
        raise PrintError("Detected textura-style codes in regular print(). Use txtra_print() instead.")
    _original_print(*args, **kwargs)

def option(resetend=True, strict=True):
    _config["resetend"] = resetend
    _config["strict"] = strict
    if strict:
        builtins.print = _strict_print
    else:
        builtins.print = _original_print

def txtra_print(text: str):
    for cls in (Fore, Back, Style):
        for key, value in cls.get_all().items():
            text = text.replace(f"{{{cls.__name__}.{key}}}", value)
    if _config["resetend"]:
        text += Style.RESET
    _original_print(text)

def txtra_format(text: str) -> str:
    for cls in (Fore, Back, Style):
        for key, value in cls.get_all().items():
            text = text.replace(f"{{{cls.__name__}.{key}}}", value)
    if _config["resetend"]:
        text += Style.RESET
    return text

# New function to list all available colors and styles
def colors_list():
    print("Foreground Colors:")
    for name, code in Fore.get_all().items():
        print(f"{code}{name}: {code}Sample Text{Style.RESET}")
    
    print("\nBackground Colors:")
    for name, code in Back.get_all().items():
        print(f"{code}{name}: {code}Sample Text{Style.RESET}")
    
    print("\nStyles:")
    for name, code in Style.get_all().items():
        print(f"{code}{name}: {code}Sample Text{Style.RESET}")
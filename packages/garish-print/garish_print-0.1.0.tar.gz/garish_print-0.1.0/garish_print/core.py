from enum import Enum

class Colour(Enum):
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    RESET = "\033[0m"

class Style(Enum):
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    INVERT = "\033[7m"
    STRIKETHROUGH = "\033[9m"
    RESET = "\033[0m"


def gprint(string, colour: Colour, *styles: Style):
    if not isinstance(colour, Colour):
        raise ValueError(f"Invalid colour argument: {colour}. Must be a member of the Colour enum.")
    
    for style in styles:
        if not isinstance(style, Style):
            raise ValueError(f"Invalid style argument: {style}. Must be a member of the Style enum.")

    style_sequence = ''.join(style.value for style in styles)
    print(f"{style_sequence}{colour.value}{string}{Colour.RESET.value}")

# 🧪 Examples
gprint("BOLD BLUE!", Colour.BLUE, Style.BOLD)
gprint("Struck through + italic green", Colour.GREEN, Style.STRIKETHROUGH, Style.ITALIC)
gprint("Blinking Bright Yellow", Colour.BRIGHT_YELLOW, Style.BLINK)
gprint("Plain Cyan", Colour.CYAN)

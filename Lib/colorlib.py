class ColorPrint:
    # code
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # style
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # bg
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Reset
    RESET = '\033[0m'
    
    @classmethod
    def black(cls, text):
        return f"{cls.BLACK}{text}{cls.RESET}"
    
    @classmethod
    def red(cls, text):
        return f"{cls.RED}{text}{cls.RESET}"
    
    @classmethod
    def green(cls, text):
        return f"{cls.GREEN}{text}{cls.RESET}"
    
    @classmethod
    def yellow(cls, text):
        return f"{cls.YELLOW}{text}{cls.RESET}"
    
    @classmethod
    def blue(cls, text):
        return f"{cls.BLUE}{text}{cls.RESET}"
    
    @classmethod
    def magenta(cls, text):
        return f"{cls.MAGENTA}{text}{cls.RESET}"
    
    @classmethod
    def cyan(cls, text):
        return f"{cls.CYAN}{text}{cls.RESET}"
    
    @classmethod
    def white(cls, text):
        return f"{cls.WHITE}{text}{cls.RESET}"
    
    @classmethod
    def bold(cls, text):
        return f"{cls.BOLD}{text}{cls.RESET}"
    
    @classmethod
    def underline(cls, text):
        return f"{cls.UNDERLINE}{text}{cls.RESET}"
    
    @classmethod
    def blink(cls, text):
        return f"{cls.BLINK}{text}{cls.RESET}"
    
    @classmethod
    def bg_red(cls, text):
        return f"{cls.BG_RED}{text}{cls.RESET}"
    
    @classmethod
    def bg_green(cls, text):
        return f"{cls.BG_GREEN}{text}{cls.RESET}"
    
    @classmethod
    def bg_blue(cls, text):
        return f"{cls.BG_BLUE}{text}{cls.RESET}"
    
    @classmethod
    def bg_yellow(cls, text):
        return f"{cls.BG_YELLOW}{text}{cls.RESET}"
    
    @classmethod
    def error(cls, text):
        return f"{cls.BOLD}{cls.RED}{text}{cls.RESET}"
    
    @classmethod
    def success(cls, text):
        return f"{cls.BOLD}{cls.GREEN}{text}{cls.RESET}"
    
    @classmethod
    def warning(cls, text):
        return f"{cls.BOLD}{cls.YELLOW}{text}{cls.RESET}"
    
    @classmethod
    def info(cls, text):
        return f"{cls.BOLD}{cls.BLUE}{text}{cls.RESET}"
    
    @classmethod
    def highlight(cls, text):
        return f"{cls.BOLD}{cls.CYAN}{text}{cls.RESET}"
    
    @classmethod
    def rainbow(cls, text):
        colors = [cls.RED, cls.YELLOW, cls.GREEN, cls.CYAN, cls.BLUE, cls.MAGENTA]
        result = ""
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            result += f"{color}{char}"
        return result + cls.RESET
def cprint(text, color=None, style=None, bg=None):
    result = text
    if color:
        result = color + result
    if style:
        result = style + result
    if bg:
        result = bg + result
    if color or style or bg:
        result += ColorPrint.RESET
    print(result)

def red(text): print(ColorPrint.red(text))
def green(text): print(ColorPrint.green(text))
def blue(text): print(ColorPrint.blue(text))
def yellow(text): print(ColorPrint.yellow(text))
def magenta(text): print(ColorPrint.magenta(text))
def cyan(text): print(ColorPrint.cyan(text))
def bold(text): print(ColorPrint.bold(text))
def error(text): print(ColorPrint.error(text))
def success(text): print(ColorPrint.success(text))
def warning(text): print(ColorPrint.warning(text))
def info(text): print(ColorPrint.info(text))
def rainbow(text): print(ColorPrint.rainbow(text))

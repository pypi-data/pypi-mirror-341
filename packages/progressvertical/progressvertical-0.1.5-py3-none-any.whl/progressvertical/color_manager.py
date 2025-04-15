from colorama import Fore, Back, Style, init

class ColorManager:
    
    RESET = Style.RESET_ALL
    
    @classmethod
    def init(cls):
        init()
    
    @classmethod
    def get_color(cls, color_type: str, name: str) -> str:
        color_map = {
            "fore": Fore,
            "back": Back,
            "style": Style
        }
        if color_type not in color_map:
            return ""
        return getattr(color_map[color_type], name.upper(), "")

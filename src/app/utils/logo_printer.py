from src.app.utils import console_colors


class LogoPrinter:

    LOGO = """
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@%%%%%%%@@@@@@@@@@,@@@@@@@@@@@@@@@@@@@
@@@@@%%%%%%%@@@@@@@@@,,@@@@@@@@@@@@@@@@@@@
@@@@@%%%%%%%@@@@@@@(,,,((@@@@@@@@@@@@@@@@@
@@@@@%%%%%%%@@@@@@,,,,,((@@@@@@@@@@@@@@@@@
@@@@@%%%%%%%@@@@@,,,,,,((@@@@@@*******@@@@
@@@@@%%%%%%%@@@,,,,,,,,,,,,,,@@*******@@@@
@@@@@%%%%%%%@@,,,,,,,,,,,,,,@@@*******@@@@
@@@@@%%%%%%%@,,,,,,,,,,,,,,@@@@*******@@@@
@@@@@%%%%%%%@@@@@@(,,,,,,,@@@@@*******@@@@
@@@@@%%%%%%%@@@@@@(,,,,,,@@@@@@*******@@@@
@@@@@%%%%%%%@@@@@@(,,,,,(@@@@@@*******@@@@
@@@@@%%%%%%%@@@@@@(,,,(((@@@@@@*******@@@@
@@@@@%%%%%%%@@@@@@(,,((((@@@@@@*******@@@@
@@@@@@@@@@@@@@@@@@@,@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""

    @staticmethod
    def print_logo():
        logo = LogoPrinter.LOGO.replace(' ', F'{console_colors.WHITE}#{console_colors.ENDC}')
        logo = logo.replace('@', ' ')
        logo = logo.replace('%', F'{console_colors.INFO}%{console_colors.ENDC}')
        logo = logo.replace(',', F'{console_colors.WARNING}%{console_colors.ENDC}')
        logo = logo.replace('(', F'{console_colors.OK}&{console_colors.ENDC}')
        logo = logo.replace('*', F'{console_colors.CYAN}&{console_colors.ENDC}')
        print(logo)

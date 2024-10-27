"""UCU MAZE GAME"""

import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

GREATING = """
            ▗▖ ▗▖ ▗▄▄▖▗▖ ▗▖   
            ▐▌ ▐▌▐▌   ▐▌ ▐▌   
            ▐▌ ▐▌▐▌   ▐▌ ▐▌   
            ▝▚▄▞▘▝▚▄▄▖▝▚▄▞▘   
        ▗▖  ▗▖ ▗▄▖ ▗▄▄▄▄▖▗▄▄▄▖
        ▐▛▚▞▜▌▐▌ ▐▌   ▗▞▘▐▌   
        ▐▌  ▐▌▐▛▀▜▌ ▗▞▘  ▐▛▀▀▘
        ▐▌  ▐▌▐▌ ▐▌▐▙▄▄▄▖▐▙▄▄▖

PRESS 'ENTER' TO CONTINUE OR 'Q' TO LEAVE
"""


def init_game_menu(stdscr) -> bool:
    """
    The starting menu of the game
    Returns:
        bool: True if user enters his name
        and presses ENTER key
    """

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    white_and_red = curses.color_pair(1)

    while True:
        stdscr.clear()
        stdscr.addstr(GREATING, white_and_red)
        stdscr.refresh()
        user_key = stdscr.getch()
        if user_key == curses.KEY_ENTER or user_key == ord('\n'):
            text_box_y = GREATING.count('\n') + 1

            stdscr.addstr(
                text_box_y, 0, "Enter your name: (hit ENTER to send)"
                )
            editwin = curses.newwin(1, 30, text_box_y + 2, 1)
            rectangle(stdscr, text_box_y + 1, 0, text_box_y + 3, 32)
            stdscr.refresh()

            box = Textbox(editwin)
            box.edit()
            user_name = box.gather().strip()
            stdscr.clear()
            stdscr.addstr(
                f"Hello {user_name}! Let's begin the jouney in mystery maze",
                curses.A_BOLD)

            stdscr.refresh()
            stdscr.getch()

            return True
        elif user_key == ord('q'):
            return False


def main(stdscr):
    """Main function"""
    if init_game_menu(stdscr):
        stdscr.clear()
        stdscr.addstr('The user accepted')
    else:
        stdscr.clear()
        stdscr.addstr('The user rejected')

    stdscr.refresh()
    stdscr.getch()


wrapper(main)

"""UCU MAZE GAME"""

import curses
import time
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
AUTHOR_INFO = """
game made by: Nikita Lenyk
my GitHub: https://github.com/ke1rro
"""
STORY = """
Something bad happened; the angry
wizard named 'SHA256' literally encrypted
everyone in UCU, and the whole territory
became an 8-bit world :(
But luckily, you didn't skip your
ПОК lessons and have made
the 'Ultra Decryptor 3000' in Castle 009.
Your task is to shoot everyone you see to decrypt them.
"""


def init_game_menu(stdscr) -> bool | str:
    """
    The starting menu of the game

    Returns:
        bool | str: False if user quites the game and
        username if user accepts
    """
    screen_lines, _ = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    white_and_red = curses.color_pair(1)

    while True:
        stdscr.clear()
        stdscr.addstr(GREATING, white_and_red | curses.A_BOLD)

        author_lines = AUTHOR_INFO.strip().split('\n')
        start_author_line = screen_lines - len(author_lines) - 1

        for i, line in enumerate(author_lines):
            stdscr.addstr(start_author_line + i,
                          0, line, white_and_red | curses.A_BOLD)

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
            stdscr.refresh()

            return user_name
        elif user_key == ord('q'):
            return False


def encrypt_the_terminal(stdscr):
    """
    Wizard deletes the message that was left to user
    """
    stdscr.clear()
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    green = curses.color_pair(2)
    pad = curses.newpad(100, 100)
    stdscr.refresh()

    for i in range(100):
        for j in range(26):
            char = chr(ord('A') + j)
            pad.addstr(char, green)

    for i in range(26):
        stdscr.clear()
        stdscr.refresh()
        pad.refresh(i, 0, 0, 0, 10, 25)
        time.sleep(0.1)


def user_interaction(stdscr):
    """
    User menu interaction
    """
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    black = curses.color_pair(3)
    if user_name := init_game_menu(stdscr):
        stdscr.clear()
        stdscr.addstr(
            f"Hello {user_name}!\n{STORY}",
            curses.A_BOLD)
        stdscr.addstr("Press 'ENTER' to continue", curses.A_BOLD)
        stdscr.refresh()
        text_box_y = STORY.count('\n')
        while True:
            user_key = stdscr.getch()
            if user_key == curses.KEY_ENTER or user_key == ord('\n'):
                for i in range(3, 0, -1):
                    stdscr.addstr(text_box_y + 1, 0, f'The wizard \
even decrypted this message it will elapse in: {i}', black | curses.A_BOLD)
                    stdscr.refresh()
                    time.sleep(1)
                stdscr.refresh()
                encrypt_the_terminal(stdscr)
                stdscr.refresh()
                break
    else:
        stdscr.clear()
        stdscr.addstr('The user rejected')
        return False
    return True


def main(stdscr):
    """Main function"""
    user_interaction(stdscr)
    stdscr.clear()
    stdscr.refresh()
    stdscr.getch()


wrapper(main)

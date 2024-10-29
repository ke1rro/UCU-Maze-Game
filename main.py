"""UCU MAZE GAME"""
import curses
import random
import signal
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

PRESS 'ENTER' TO CONTINUE OR 'Q' TO QUIT
   USE ONLY ENGLISH KEYBOARD LAYOUT
"""
LOSE = """
        ▗▖  ▗▖▗▄▖ ▗▖ ▗▖
         ▝▚▞▘▐▌ ▐▌▐▌ ▐▌
          ▐▌ ▐▌ ▐▌▐▌ ▐▌
          ▐▌ ▝▚▄▞▘▝▚▄▞▘
        ▗▖    ▗▄▖  ▗▄▄▖▗▄▄▄▖
        ▐▌   ▐▌ ▐▌▐▌   ▐▌
        ▐▌   ▐▌ ▐▌ ▝▀▚▖▐▛▀▀▘
        ▐▙▄▄▖▝▚▄▞▘▗▄▄▞▘▐▙▄▄▖
PRESS 'R' to RESTART or hit 'Q' TWICE(slowly) to QUIT
"""
WIN = """

        ▗▖  ▗▖▗▄▖ ▗▖ ▗▖
         ▝▚▞▘▐▌ ▐▌▐▌ ▐▌
          ▐▌ ▐▌ ▐▌▐▌ ▐▌
          ▐▌ ▝▚▄▞▘▝▚▄▞▘
        ▗▖ ▗▖▗▄▄▄▖▗▖  ▗▖
        ▐▌ ▐▌  █  ▐▛▚▖▐▌
        ▐▌ ▐▌  █  ▐▌ ▝▜▌
        ▐▙█▟▌▗▄█▄▖▐▌  ▐▌
Press 'ENTER' and you to comeback to the game menu
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
TO WIN decrypt ALL '?' into people
and find the exit from maze
YOU LOSE if you don't have enough ammo
to decrypt everyone or the '?' encrypt you
PS. You are displayed as '00' and your enemies is '?'
"""
GAME_GUIDE = """
'WASD' - to move 'SPACE' - to shoot
'ESC' twice(slowly) - TO QUIT
To CHANGE the shooting direction use '1', '2', '3', '4'
"""
WIDTH = 19
HEIGTH = 15


def ignore_ctrl_c():
    """
    Ignoring CTRL+C, to avoid errors in game runtime
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def init_game_menu(stdscr) -> bool | str:
    """
    The starting menu of the game

    Returns:
        bool | str: False if user quits the game, and
        username if the user accepts
    """
    screen_lines, _ = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    white_and_red = curses.color_pair(1)
    invalid_input = [' ', '', '\n']

    user_name = ''
    while not user_name:
        stdscr.clear()
        stdscr.addstr(GREATING, white_and_red | curses.A_BOLD)

        author_lines = AUTHOR_INFO.strip().split('\n')
        start_author_line = screen_lines - len(author_lines) - 1

        for i, line in enumerate(author_lines):
            stdscr.addstr(start_author_line + i, 0,
                          line, white_and_red | curses.A_BOLD)

        stdscr.refresh()

        user_key = stdscr.getkey()

        if user_key == '\n':
            text_box_y = GREATING.count('\n') + 1
            stdscr.addstr(
                text_box_y, 0, "Enter your name: (hit ENTER to send)"
                )
            editwin = curses.newwin(1, 30, text_box_y + 2, 1)
            rectangle(stdscr, text_box_y + 1, 0, text_box_y + 3, 32)
            stdscr.refresh()

            # Gets username
            box = Textbox(editwin)
            box.edit()
            user_name = box.gather().strip()
            if user_name in invalid_input:
                continue
            stdscr.clear()
            stdscr.refresh()

        elif user_key.lower() == 'q':
            return False

    return user_name


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
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)

    red = curses.color_pair(3)
    blue = curses.color_pair(5)

    if user_name := init_game_menu(stdscr):
        stdscr.clear()
        stdscr.addstr(
            f"Hello {user_name}!\n{STORY}",
            curses.A_BOLD)

        stdscr.addstr("Press 'ENTER' to continue", curses.A_BOLD | blue)
        stdscr.refresh()

        text_box_y = STORY.count('\n')

        while True:
            user_key = stdscr.getkey().lower()
            if user_key == '\n':
                for i in range(5, 0, -1):
                    stdscr.addstr(text_box_y + 1, 0, f'The wizard \
even encrypted this message it \
will be destroyed in: {i}', red | curses.A_BOLD)
                    stdscr.refresh()
                    time.sleep(1)
                stdscr.refresh()
                encrypt_the_terminal(stdscr)
                stdscr.refresh()
                break
    else:
        stdscr.clear()
        stdscr.addstr('Press any key to leave')
        return False
    return True


def carve_maze(x, y, maze):
    """
    Recursive function to carve out paths in the maze
    using DFS(depth-first search)
    """
    # The values 0, 1, 2, and 3 will represent
    # "right", "down", "left", and "up" respectively
    directions = [0, 1, 2, 3]
    random.shuffle(directions)

    for direction in directions:
        # dx - direction x
        # dy - drection y
        dx, dy = 0, 0

        # Set the movement offsets based on the current direction
        if direction == 0:
            dx = 1
        elif direction == 1:
            dy = 1
        elif direction == 2:
            dx = -1
        else:
            dy = -1

        x1 = x + dx
        y1 = y + dy
        x2 = x1 + dx
        y2 = y1 + dy

        if 0 < x2 < WIDTH and 0 < y2 < HEIGTH:
            if maze[x1][y1] == 1 and maze[x2][y2] == 1:
                maze[x1][y1] = 0
                maze[x2][y2] = 0
                carve_maze(x2, y2, maze)


def generate_maze():
    """
    Generate the maze starting from a given cell
    """
    # random.seed()
    maze = [[1 for _ in range(HEIGTH)] for _ in range(WIDTH)]
    maze[1][1] = 0
    carve_maze(1, 1, maze)
    # Enterance to the maze
    maze[1][0] = 0
    # Exit from the maze
    maze[WIDTH - 2][HEIGTH - 1] = 0
    return maze


def display_maze(stdscr, maze: list[list[int]],
                 enemies:  list[tuple[int]]):
    """
    Display the generated maze on the screen
    """
    stdscr.clear()
    stdscr.move(0, 0)
    for y in range(HEIGTH):
        for x in range(WIDTH):
            if maze[x][y] == 0:
                stdscr.addstr("  ", curses.color_pair(1))
            else:
                stdscr.addstr("[]", curses.color_pair(1))
        stdscr.addstr("\n")

    for enemy in enemies:
        stdscr.addstr(enemy[1], enemy[0] * 2, '?', curses.color_pair(2))
    stdscr.refresh()


def display_user(stdscr, y, x):
    """
    Displays user as 00 on the screen
    """
    stdscr.addstr(y, x, "OO", curses.color_pair(2))
    stdscr.refresh()


def place_enemies(maze: list[list[int]],
                  num_enemies: int) -> list[tuple[int]]:
    """Randomly place enemies in the maze."""
    enemies = []
    while len(enemies) < num_enemies:
        x = random.randint(1, WIDTH - 2)
        y = random.randint(1, HEIGTH - 2)
        if maze[x][y] == 0 and (x, y) not in enemies:
            enemies.append((x, y))
    return enemies


def display_game_info(stdscr, bullets: int,
                      enemies_count: int, direction: str):
    """
    Displaying game interface
    """
    stdscr.addstr(HEIGTH + 1, 0,
                  f'Bullets left: {bullets:<3}', curses.A_BOLD)
    stdscr.addstr(HEIGTH + 2, 0,
                  f'Enemies left: {enemies_count:<3}', curses.A_BOLD)

    arrow = ' '
    if direction == 'up':
        arrow = '↑'
    elif direction == 'down':
        arrow = '↓'
    elif direction == 'left':
        arrow = '←'
    elif direction == 'right':
        arrow = '→'

    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.addstr(HEIGTH + 3, 0, f'Direction: {arrow}', curses.color_pair(2))
    stdscr.addstr(HEIGTH + 4, 0, GAME_GUIDE, curses.color_pair(6))


def show_lose_message(stdscr):
    """
    Prints 'YOU LOSE' on screen
    """
    stdscr.clear()
    stdscr.addstr(LOSE)
    stdscr.refresh()
    while True:
        key = stdscr.getkey().lower()
        if key == 'r':
            return 'restart'
        if key == 'q':
            return 'quit'


def mainloop(stdscr, maze: list[list[int]],
             bullets: int, enemies: list[tuple[int]]):
    """
    Mainloop for user's interaction with game
    """
    y = 1
    m = 2
    x = 1
    last_direction = ''
    bullets_remaining = bullets
    bullets_list = []
    stdscr.nodelay(True)
    stdscr.clear()
    display_maze(stdscr, maze, enemies)
    display_user(stdscr, y, m)

    bullets_list = []
    touched_enemy = False
    no_bullets = False
    runaway = False

    while not touched_enemy and not no_bullets and not runaway:
        try:
            key = stdscr.getkey().lower()
        except Exception:
            key = None

        if key == '\x1b':
            return 'menu'

        stdscr.addstr(y, m, "  ", curses.color_pair(2))

        if key == '1':
            last_direction = 'left'
        elif key == '2':
            last_direction = 'right'
        elif key == '3':
            last_direction = 'up'
        elif key == '4':
            last_direction = 'down'

        if key == 'a' and maze[x - 1][y] == 0:
            last_direction = 'left'
            x -= 1
            m -= 2
        elif key == 'd' and maze[x + 1][y] == 0:
            last_direction = 'right'
            x += 1
            m += 2
        elif key == 'w' and maze[x][y - 1] == 0:
            last_direction = 'up'
            y -= 1
        elif key == 's' and maze[x][y + 1] == 0:
            last_direction = 'down'
            y += 1

        if key == ' ' and bullets_remaining > 0:
            bullets_remaining -= 1

            # One list represent single bullet where,
            # first x, y the currrent coordinates of bullet,
            # the last x, y represnt the previous coordinates of bullet
            bullets_list.append([
                x, y,
                last_direction,
                x, y
            ])

        # Iterates through list of tuples to get bullet info
        for bullet in bullets_list[:]:
            stdscr.addstr(bullet[4], bullet[3] * 2, "  ")

            if bullet[2] == 'left':
                bullet[0] -= 1
            elif bullet[2] == 'right':
                bullet[0] += 1
            elif bullet[2] == 'up':
                bullet[1] -= 1
            elif bullet[2] == 'down':
                bullet[1] += 1

            bullet[3], bullet[4] = bullet[0], bullet[1]

            bx, by = bullet[0], bullet[1]

            if 0 <= bx < WIDTH and 0 <= by < HEIGTH:
                if maze[bx][by] == 1:
                    bullets_list.remove(bullet)
                # Checks if bullets hitted the enemy
                elif (bx, by) in enemies:
                    maze[bx][by] = 0
                    stdscr.addstr(by, bx * 2, "  ")
                    enemies.remove((bx, by))
                    bullets_list.remove(bullet)
            else:
                bullets_list.remove(bullet)

        display_user(stdscr=stdscr, y=y, x=m)
        display_game_info(stdscr, bullets_remaining,
                          len(enemies), last_direction)

        for bullet in bullets_list:
            stdscr.addstr(bullet[1], bullet[0] * 2,
                          "*", curses.color_pair(2))

        if (x, y) in enemies:
            touched_enemy = True
            stdscr.nodelay(False)

        # Only check if no bullets are currently fired
        if len(bullets_list) == 0:
            if bullets_remaining < len(enemies):
                no_bullets = True
                stdscr.nodelay(False)

        # Checks for winning condition
        if len(enemies) == 0 and (x, y) == (WIDTH - 2, HEIGTH - 1):
            stdscr.clear()
            stdscr.addstr(WIN)
            stdscr.refresh()
            # Pause before returning to menu
            time.sleep(3)
            return 'menu'

        # Checks if user trying to runaway
        if len(enemies) > 0 and (x, y) == (WIDTH - 2, HEIGTH - 1):
            runaway = True
            stdscr.nodelay(False)

        stdscr.refresh()
        time.sleep(0.1)

    if touched_enemy:
        action = show_lose_message(stdscr)
        if action == 'restart':
            start_game(stdscr)
        else:
            return 'menu'

    if no_bullets:
        action = show_lose_message(stdscr)
        if action == 'restart':
            start_game(stdscr)
        else:
            return 'menu'

    if runaway:
        action = show_lose_message(stdscr)
        if action == 'restart':
            start_game(stdscr)
        else:
            return 'menu'


def start_game(stdscr):
    """
    Starts the game if user lost and pressed 'R'
    """
    bullets = random.randint(6, 10)
    maze = generate_maze()
    enemies = place_enemies(maze, random.randint(6, bullets))
    stdscr.clear()
    result = mainloop(stdscr, maze, bullets, enemies)
    stdscr.nodelay(False)
    if result == 'menu':
        return result


def main(stdscr):
    """
    Entry point
    """
    while True:
        stdscr.clear()
        stdscr.refresh()
        if user_interaction(stdscr):
            stdscr.clear()
            if start_game(stdscr):
                continue
            stdscr.refresh()
            stdscr.getch()
        else:
            break


if __name__ == '__main__':
    ignore_ctrl_c()
    wrapper(main)

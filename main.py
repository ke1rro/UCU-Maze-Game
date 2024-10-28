"""UCU MAZE GAME"""
import random
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

PRESS 'ENTER' TO CONTINUE OR 'Q' TO QUIT
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
PRESS 'R' to RESTART or 'Q' to QUIT
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
Your task is to shoot EVERYONE you see to decrypt them.
AND FIND THE ESCAPE FROM THE MAZE
PS. You are displayed as '00' and your enemies is '?'
"""
GAME_GUIDE = """
'WASD' - to move
'SPACE' - to shoot
'ESC' - TO QUIT
To CHANGE the shooting direction use
'1', '2', '3', '4'
TO WIN decrypt ALL '?' into people
and find the exit from maze
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
    invalid_input = [' ', '', '\n']

    user_name = ''
    while not user_name:
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
            if user_name in invalid_input:
                continue
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
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    red = curses.color_pair(3)
    green = curses.color_pair(4)
    blue = curses.color_pair(5)
    if user_name := init_game_menu(stdscr):
        stdscr.clear()
        stdscr.addstr(
            f"Hello {user_name}!\n{STORY}",
            curses.A_BOLD)
        stdscr.addstr(f'{GAME_GUIDE}', green)
        stdscr.addstr("Press 'ENTER' to continue", curses.A_BOLD | blue)
        stdscr.refresh()
        text_box_y = STORY.count('\n')
        while True:
            user_key = stdscr.getch()
            if user_key == curses.KEY_ENTER or user_key == ord('\n'):
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


width = 19
height = 15

maze = [[1 for _ in range(height)] for _ in range(width)]
enemies = []

bullets = random.randint(6, 12)


def carve_maze(x, y):
    """Recursive function to carve out paths in the maze."""
    directions = [0, 1, 2, 3]
    random.shuffle(directions)

    for dir in directions:
        dx, dy = 0, 0
        if dir == 0:
            dx = 1
        elif dir == 1:
            dy = 1
        elif dir == 2:
            dx = -1
        else:
            dy = -1

        x1 = x + dx
        y1 = y + dy
        x2 = x1 + dx
        y2 = y1 + dy

        if 0 < x2 < width and 0 < y2 < height:
            if maze[x1][y1] == 1 and maze[x2][y2] == 1:
                maze[x1][y1] = 0
                maze[x2][y2] = 0
                carve_maze(x2, y2)


def generate_maze():
    """Generate the maze starting from a given cell."""
    random.seed()
    maze[1][1] = 0
    carve_maze(1, 1)
    maze[1][0] = 0
    maze[width - 2][height - 1] = 0


def display_maze(stdscr):
    """Display the generated maze on the screen."""
    stdscr.clear()
    stdscr.move(0, 0)
    for y in range(height):
        for x in range(width):
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


def place_enemies(num_enemies: int):
    """Randomly place enemies in the maze."""
    while len(enemies) < num_enemies:
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        if maze[x][y] == 0 and (x, y) not in enemies:
            enemies.append((x, y))


def display_game_info(stdscr, bullets: int,
                      enemies_count: int, direction: str):
    stdscr.addstr(height + 1, 0,
                  f'Bullets left: {bullets}', curses.A_BOLD)
    stdscr.addstr(height + 2, 0,
                  f'Enemies left: {enemies_count}', curses.A_BOLD)

    arrow = ' '
    if direction == 'up':
        arrow = '↑'
    elif direction == 'down':
        arrow = '↓'
    elif direction == 'left':
        arrow = '←'
    elif direction == 'right':
        arrow = '→'

    stdscr.addstr(height + 3, 0, f'Direction: {arrow}', curses.color_pair(2))


def show_lose_message(stdscr):
    stdscr.clear()
    stdscr.addstr(LOSE)
    stdscr.refresh()
    while True:
        key = stdscr.getkey().lower()
        if key == 'r':
            start_game(stdscr)
        if key == 'q':
            break


def mainloop(stdscr):
    y = 1
    m = 2
    x = 1
    last_direction = ''
    bullets_remaining = bullets

    stdscr.nodelay(True)
    stdscr.clear()
    display_maze(stdscr)
    display_user(stdscr, y, m)

    bullets_list = []
    touched_enemy = False

    while not touched_enemy:
        try:
            key = stdscr.getkey().lower()
        except Exception:
            key = None

        if key == '\x1b':
            return

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
            bullets_list.append({
                "x": x, "y": y,
                "direction": last_direction,
                "prev_x": x, "prev_y": y
            })

        for bullet in bullets_list[:]:
            stdscr.addstr(bullet["prev_y"], bullet["prev_x"] * 2, "  ")

            if bullet["direction"] == 'left':
                bullet["x"] -= 1
            elif bullet["direction"] == 'right':
                bullet["x"] += 1
            elif bullet["direction"] == 'up':
                bullet["y"] -= 1
            elif bullet["direction"] == 'down':
                bullet["y"] += 1

            bullet["prev_x"], bullet["prev_y"] = bullet["x"], bullet["y"]

            bx, by = bullet["x"], bullet["y"]

            if 0 <= bx < width and 0 <= by < height:
                if maze[bx][by] == 1:
                    bullets_list.remove(bullet)
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
            stdscr.addstr(bullet["y"], bullet["x"] * 2,
                          "*", curses.color_pair(2))

        if (x, y) in enemies:
            touched_enemy = True
            stdscr.nodelay(False)

        stdscr.refresh()
        time.sleep(0.1)

    if touched_enemy or bullets_remaining == 0:
        show_lose_message(stdscr)


def start_game(stdscr):
    """Start the game if user lost and pressed 'R'"""
    global bullets, maze
    maze = [[1 for _ in range(height)] for _ in range(width)]
    bullets = random.randint(6, 12)
    stdscr.clear()
    generate_maze()
    place_enemies(6)
    mainloop(stdscr)


def main(stdscr):
    """Main function"""
    while True:
        try:
            stdscr.clear()
            stdscr.refresh()

            if user_interaction(stdscr):
                stdscr.clear()
                start_game(stdscr)
                stdscr.refresh()
                stdscr.getch()
            else:
                break
        except KeyboardInterrupt:
            continue


wrapper(main)

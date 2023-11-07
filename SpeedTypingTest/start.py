import curses, time
from curses import wrapper


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to the Speed Typing Test", curses.color_pair(1))
    stdscr.addstr(1, 0, "\nPress any key to continue.", curses.color_pair(2))
    stdscr.refresh()
    stdscr.getch()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def wpm_test(stdscr):
    with open("text.txt", "r") as file:
        target_text = file.read()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        if key in (str(curses.KEY_BACKSPACE), "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

        if len(current_text) == len(target_text):
            break

    written_text = " ".join(current_text)
    correct_words = 0
    for i in range(len(target_text)):
        if target_text[i] == written_text[i]:
            correct_words += 1
    wpm = round((len(written_text) / (time_elapsed / 60)) / 5)
    time.sleep(1.5)
    stdscr.addstr(1, 0, f"Twoje WPM: {wpm}")
    stdscr.addstr(2, 0, f"Ilość poprawnie wpisanych wyrazów: {correct_words}")
    stdscr.addstr(3, 0, "Naciśnij ESC, aby zakończyć.")

    while key != 27:
        key = stdscr.getch()


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    wpm_test(stdscr)


curses.wrapper(main)

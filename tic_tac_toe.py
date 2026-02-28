import tkinter as tk
from tkinter import messagebox
import math
import random

# ---------------- CONSTANTS ----------------
HUMAN = "X"
AI = "O"
EMPTY = ""

COLOR_BG = "#2b2b2b"
COLOR_BTN = "#3c3f41"
COLOR_HUMAN = "#ffde57"
COLOR_AI = "#4584b6"
COLOR_TEXT = "#ffffff"

# ---------------- GAME STATE ----------------
board = [[EMPTY]*3 for _ in range(3)]
game_over = False
scores = {"X": 0, "O": 0, "D": 0}
difficulty = "Hard"

# ---------------- LOGIC FUNCTIONS ----------------
def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    if all(cell != EMPTY for row in board for cell in row):
        return "D"
    return None


def minimax(is_max):
    result = check_winner()
    if result == AI:
        return 1
    if result == HUMAN:
        return -1
    if result == "D":
        return 0

    if is_max:
        best = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = AI
                    best = max(best, minimax(False))
                    board[r][c] = EMPTY
        return best
    else:
        best = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = HUMAN
                    best = min(best, minimax(True))
                    board[r][c] = EMPTY
        return best


# ---------------- AI MOVES ----------------
def random_ai_move():
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = AI
        buttons[r][c].config(text=AI, bg=COLOR_AI)
        end_turn()


def best_ai_move():
    best_score = -math.inf
    move = None

    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                board[r][c] = AI
                score = minimax(False)
                board[r][c] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (r, c)

    if move:
        r, c = move
        board[r][c] = AI
        buttons[r][c].config(text=AI, bg=COLOR_AI)
        end_turn()


def ai_move():
    if difficulty == "Easy":
        random_ai_move()
    elif difficulty == "Medium":
        if random.choice([True, False]):
            random_ai_move()
        else:
            best_ai_move()
    else:
        best_ai_move()


# ---------------- UI INTERACTION ----------------
def button_click(r, c):
    global game_over
    if board[r][c] != EMPTY or game_over:
        return

    board[r][c] = HUMAN
    buttons[r][c].config(text=HUMAN, bg=COLOR_HUMAN)
    end_turn(ai=True)


def end_turn(ai=False):
    global game_over
    result = check_winner()

    if result:
        game_over = True
        scores[result] += 1
        update_score()
        show_emoji(result)
        messagebox.showinfo("Game Over",
                            "Draw!" if result == "D" else f"{result} wins!")
        return

    if ai:
        status_label.config(text="AI thinking...")
        window.after(300, ai_move)
    else:
        status_label.config(text="Your turn")


def reset_game():
    global game_over
    game_over = False
    status_label.config(text="Your turn")
    emoji_label.config(text="")
    for r in range(3):
        for c in range(3):
            board[r][c] = EMPTY
            buttons[r][c].config(text="", bg=COLOR_BTN)


def update_score():
    score_label.config(
        text=f"X: {scores['X']}   O: {scores['O']}   Draws: {scores['D']}"
    )


# ---------------- EMOJI ANIMATION ----------------
def show_emoji(result):
    if result == HUMAN:
        emoji = "🧑🎉"
    elif result == AI:
        emoji = "🤖🏆"
    else:
        emoji = "😐"

    emoji_label.config(text=emoji)

    def clear():
        emoji_label.config(text="")

    window.after(2000, clear)


# ---------------- DIFFICULTY ----------------
def set_level(*args):
    global difficulty
    difficulty = level_var.get()


# ---------------- UI SETUP ----------------
window = tk.Tk()
window.title("Tic Tac Toe - AI")
window.config(bg=COLOR_BG)
window.resizable(False, False)

status_label = tk.Label(window, text="Your turn",
                        font=("Arial", 14),
                        bg=COLOR_BG, fg=COLOR_TEXT)
status_label.grid(row=0, column=0, columnspan=3, pady=5)

buttons = [[None]*3 for _ in range(3)]
for r in range(3):
    for c in range(3):
        btn = tk.Button(window,
                        text="",
                        font=("Arial", 32, "bold"),
                        width=4, height=2,
                        bg=COLOR_BTN,
                        fg=COLOR_TEXT,
                        command=lambda r=r, c=c: button_click(r, c))
        btn.grid(row=r+1, column=c, padx=5, pady=5)
        buttons[r][c] = btn

score_label = tk.Label(window, text="X: 0   O: 0   Draws: 0",
                       font=("Arial", 12),
                       bg=COLOR_BG, fg=COLOR_TEXT)
score_label.grid(row=4, column=0, columnspan=3, pady=5)

reset_btn = tk.Button(window, text="Restart",
                      font=("Arial", 12),
                      command=reset_game)
reset_btn.grid(row=5, column=0, columnspan=3, pady=5)

emoji_label = tk.Label(window, text="", font=("Arial", 40), bg=COLOR_BG)
emoji_label.grid(row=6, column=0, columnspan=3)

level_var = tk.StringVar(value="Hard")
level_menu = tk.OptionMenu(window, level_var, "Easy", "Medium", "Hard")
level_menu.grid(row=7, column=0, columnspan=3, pady=5)
level_var.trace("w", set_level)

if __name__ == "__main__":
    window.mainloop()

import tkinter as tk
import time
import random

# ===== 基本設定 =====
SIZE = 300
CELL = 100
TIME_LIMIT = 30

root = tk.Tk()
root.title("OOXX 限時對戰（玩家 vs 電腦）")

canvas = tk.Canvas(root, width=SIZE, height=SIZE + 80, bg="white")
canvas.pack()

# ===== 遊戲狀態 =====
board = [["" for _ in range(3)] for _ in range(3)]
game_over = False
start_time = time.time()
score = {"O": 0, "X": 0}

# ===== 畫棋盤 =====
def draw_board():
    for i in range(1, 3):
        canvas.create_line(i * CELL, 0, i * CELL, SIZE, width=4)
        canvas.create_line(0, i * CELL, SIZE, i * CELL, width=4)

# ===== 畫棋子 =====
def draw_o(r, c):
    canvas.create_oval(
        c * CELL + 20, r * CELL + 20,
        (c + 1) * CELL - 20, (r + 1) * CELL - 20,
        width=4, outline="blue"
    )

def draw_x(r, c):
    canvas.create_line(
        c * CELL + 20, r * CELL + 20,
        (c + 1) * CELL - 20, (r + 1) * CELL - 20,
        width=4, fill="red"
    )
    canvas.create_line(
        c * CELL + 20, (r + 1) * CELL - 20,
        (c + 1) * CELL - 20, r * CELL + 20,
        width=4, fill="red"
    )

# ===== 檢查勝負 =====
def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]

    return None

# ===== 電腦下棋 =====
def computer_move():
    empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ""]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = "X"
        draw_x(r, c)

# ===== 更新資訊 =====
def update_info():
    canvas.delete("info")
    left = TIME_LIMIT - int(time.time() - start_time)
    canvas.create_text(
        SIZE / 2, SIZE + 20,
        text=f"剩餘時間：{left}s   玩家(O)：{score['O']}  電腦(X)：{score['X']}",
        font=("Arial", 12),
        tags="info"
    )

    if left <= 0 and not game_over:
        end_game("時間到！")

# ===== 滑鼠點擊 =====
def click(event):
    global game_over

    if game_over:
        restart()
        return

    r = event.y // CELL
    c = event.x // CELL

    if r >= 3 or c >= 3 or board[r][c] != "":
        return

    # 玩家下 O
    board[r][c] = "O"
    draw_o(r, c)

    winner = check_winner()
    if winner:
        score[winner] += 1
        end_game("你贏了！")
        return

    # 電腦下 X
    computer_move()

    winner = check_winner()
    if winner:
        score[winner] += 1
        end_game("電腦獲勝！")
        return

    if all(board[r][c] != "" for r in range(3) for c in range(3)):
        end_game("平手！")

# ===== 結束遊戲 =====
def end_game(text):
    global game_over
    game_over = True
    canvas.create_text(
        SIZE / 2, SIZE / 2,
        text=f"{text}\n點擊重新開始",
        font=("Arial", 16),
        fill="purple"
    )

# ===== 重新開始 =====
def restart():
    global board, game_over, start_time
    canvas.delete("all")
    board = [["" for _ in range(3)] for _ in range(3)]
    game_over = False
    start_time = time.time()
    draw_board()
    update_info()

# ===== 啟動 =====
canvas.bind("<Button-1>", click)
draw_board()
update_info()

def timer():
    update_info()
    root.after(1000, timer)

timer()
root.mainloop()

import tkinter as tk
import time
import random

SIZE = 300
CELL = 100
LINE_WIDTH = 4

root = tk.Tk()
root.title("OOXX 對戰電腦")

canvas = tk.Canvas(root, width=SIZE, height=SIZE + 40, bg="white")
canvas.pack()

board = [["" for _ in range(3)] for _ in range(3)]
game_over = False
start_time = time.time()

def draw_board():
    for i in range(1, 3):
        canvas.create_line(i * CELL, 0, i * CELL, SIZE, width=LINE_WIDTH)
        canvas.create_line(0, i * CELL, SIZE, i * CELL, width=LINE_WIDTH)

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

def check_winner():
    lines = []

    for i in range(3):
        lines.append([(i,0),(i,1),(i,2)])
        lines.append([(0,i),(1,i),(2,i)])

    lines.append([(0,0),(1,1),(2,2)])
    lines.append([(0,2),(1,1),(2,0)])

    for line in lines:
        a,b,c = line
        if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]] != "":
            return board[a[0]][a[1]], line
    return None, None

def draw_win_line(line):
    (r1,c1),_,(r3,c3) = line
    canvas.create_line(
        c1*CELL+50, r1*CELL+50,
        c3*CELL+50, r3*CELL+50,
        width=6, fill="green"
    )

def computer_move():
    empty = [(r,c) for r in range(3) for c in range(3) if board[r][c] == ""]
    if empty:
        r,c = random.choice(empty)
        board[r][c] = "X"
        draw_x(r,c)

def click(event):
    global game_over

    if game_over:
        restart()
        return

    c = event.x // CELL
    r = event.y // CELL
    if r>=3 or c>=3 or board[r][c]!="":
        return

    board[r][c] = "O"
    draw_o(r,c)

    winner, line = check_winner()
    if winner:
        draw_win_line(line)
        show_result("你贏了！")
        return

    computer_move()

    winner, line = check_winner()
    if winner:
        draw_win_line(line)
        show_result("電腦獲勝！")
        return

    if all(board[r][c] != "" for r in range(3) for c in range(3)):
        show_result("平手！")

def show_result(text):
    global game_over
    game_over = True
    t = int(time.time() - start_time)
    canvas.create_text(
        SIZE/2, SIZE/2,
        text=f"{text}\n耗時 {t} 秒\n點擊重新開始",
        font=("Arial",16),
        fill="purple"
    )

def restart():
    global board, game_over, start_time
    canvas.delete("all")
    board = [["" for _ in range(3)] for _ in range(3)]
    game_over = False
    start_time = time.time()
    draw_board()

canvas.bind("<Button-1>", click)
draw_board()
root.mainloop()

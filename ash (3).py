import tkinter as tk      # 匯入 Tkinter，建立視窗
import time               # 匯入 time，用來計時

# ===== 基本設定 =====
SIZE = 300                # 視窗大小
CELL = 100                # 每一格大小（300 / 3）
LINE_WIDTH = 4            # 格線粗細

# ===== 建立主視窗 =====
root = tk.Tk()            # 建立視窗物件
root.title("OOXX 井字遊戲")  # 設定視窗標題

# 建立畫布（畫棋盤、O、X）
canvas = tk.Canvas(root, width=SIZE, height=SIZE + 40, bg="white")
canvas.pack()

# ===== 遊戲狀態 =====
board = [["" for _ in range(3)] for _ in range(3)]  # 3x3 棋盤
game_over = False          # 是否結束
start_time = time.time()   # 記錄遊戲開始時間

# ===== 畫棋盤 =====
def draw_board():
    # 畫直線
    for i in range(1, 3):
        canvas.create_line(
            i * CELL, 0, i * CELL, SIZE,
            width=LINE_WIDTH
        )
    # 畫橫線
    for i in range(1, 3):
        canvas.create_line(
            0, i * CELL, SIZE, i * CELL,
            width=LINE_WIDTH
        )

# ===== 畫 O =====
def draw_o(row, col):
    x1 = col * CELL + 20
    y1 = row * CELL + 20
    x2 = (col + 1) * CELL - 20
    y2 = (row + 1) * CELL - 20
    canvas.create_oval(x1, y1, x2, y2, width=4)

# ===== 畫 X =====
def draw_x(row, col):
    x1 = col * CELL + 20
    y1 = row * CELL + 20
    x2 = (col + 1) * CELL - 20
    y2 = (row + 1) * CELL - 20
    canvas.create_line(x1, y1, x2, y2, width=4)
    canvas.create_line(x1, y2, x2, y1, width=4)

# ===== 檢查勝負 =====
def check_winner():
    # 檢查橫列與直行
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]

    # 檢查對角線
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]

    return None

# ===== 顯示結束畫面 =====
def show_result(text):
    global game_over
    game_over = True

    elapsed = int(time.time() - start_time)  # 計算耗時

    canvas.create_text(
        SIZE / 2, SIZE / 2,
        text=f"{text}\n耗時：{elapsed} 秒\n左鍵重新開始",
        font=("Arial", 16),
        fill="red"
    )

# ===== 滑鼠點擊處理 =====
def click(event):
    global game_over

    # 如果遊戲結束 → 左鍵重新開始
    if game_over:
        restart()
        return

    # 判斷點到哪一格
    col = event.x // CELL
    row = event.y // CELL

    # 超出棋盤不處理
    if row >= 3 or col >= 3:
        return

    # 已經有棋子就不能放
    if board[row][col] != "":
        return

    # 左鍵放 O
    if event.num == 1:
        board[row][col] = "O"
        draw_o(row, col)

    # 右鍵放 X
    elif event.num == 3:
        board[row][col] = "X"
        draw_x(row, col)

    # 檢查是否有人獲勝
    winner = check_winner()
    if winner:
        show_result(f"{winner} 獲勝！")
        return

    # 檢查是否平手
    if all(board[r][c] != "" for r in range(3) for c in range(3)):
        show_result("平手！")

# ===== 重新開始 =====
def restart():
    global board, game_over, start_time

    canvas.delete("all")    # 清空畫面
    board = [["" for _ in range(3)] for _ in range(3)]
    game_over = False
    start_time = time.time()

    draw_board()

# ===== 綁定滑鼠事件 =====
canvas.bind("<Button-1>", click)   # 左鍵
canvas.bind("<Button-3>", click)   # 右鍵

# ===== 啟動遊戲 =====
draw_board()
root.mainloop()

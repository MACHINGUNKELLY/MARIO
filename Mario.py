import tkinter as tk
import random
from tkinter import messagebox

obstacles = []

speed_mod = 0
def move_obstacles():# сдвиг препятсвий
    global obstacles, canvas, world_speed
    for obstacle in obstacles:
        canvas.move(obstacle[0], world_speed, 0)
        obstacle[1][0] += world_speed
        x = canvas.coords(obstacle[0])[0]
        if x < -100:
            new_x = random.randint(800, 900)
            canvas.move(obstacle[0], new_x - canvas.coords(obstacle[0])[0], 0)
            obstacle[1][0] = new_x
        check_player_coll(obstacle)
    canvas.after(10, move_obstacles)


def check_player_coll(obstacle):# проверки встречи игрока и препятствий
    global player, on_box, stand_box, stop
    if obstacle[1][0] == 154:
        y = canvas.coords(player)[1]
        if obstacle[1][1] - 50 <= y:
            stop = True
            messagebox.showinfo("Проигрыш", """                 Вы проиграли
Закройте это окно чтобы начать заново""")
            reset_game()
            stop = False
    if canvas.coords(player)[0] - 60 < obstacle[1][0] < canvas.coords(player)[0] + 74:
        on_box = True
        stand_box = obstacle[0]
    elif stand_box == obstacle[0]:
        on_box = False
        stand_box = None
        canvas.move(player, 0, 60)


def update_score():# обновление очков и скорости
    global score, score_label, world_speed
    score += 1
    score_label.config(text="Score: " + str(score))
    if score > 10000:
        world_speed = -4
    elif score > 5000:
        world_speed =-3
    elif score > 1000:
        world_speed = -2
    else:
        world_speed = -1


def move_background():# сдвиг задника
    global world_speed, stop
    if not stop:
        canvas.move(background, world_speed, 0)
        x1, y1, x2, y2 = canvas.bbox(background)
        if x2 - 750 <= 0:
            canvas.move(background, screen_width / 3, 0)
        update_score()
    canvas.after(10, move_background)


jump_tick = 0


def jump_continue():
    global jump_tick
    canvas.move(player, 0, -10)
    jump_tick += 1

    # Плавный прыжок вверх
    if jump_tick >= 10:
        jump_tick = 0
        canvas.after(10, fall)  # Запуск приземления через 10 миллисекунд
    else:
        canvas.after(10 + 2 * jump_tick, jump_continue)


def jump():# прыжок
    global double_jump
    if not double_jump:# проверка на повторное нажатие
        double_jump = True
        canvas.after(10, jump_continue())


def reset_game():# сброс препятсвий и очков
    global obstacles, score, player, stand_box, on_box, double_jump
    score = 0
    canvas.move(player, -canvas.coords(player)[0] + 100, -canvas.coords(player)[1] + 422 - 105)
    stand_box = None
    on_box = False
    double_jump = False
    canvas.move(obstacles[0][0], 300 - obstacles[0][1][0], 0)
    canvas.move(obstacles[1][0], 500 - obstacles[1][1][0], 0)
    canvas.move(obstacles[2][0], 700 - obstacles[2][1][0], 0)
    canvas.move(obstacles[3][0], 900 - obstacles[3][1][0], 0)
    obstacles[0][1][0] = 300
    obstacles[1][1][0] = 500
    obstacles[2][1][0] = 700
    obstacles[3][1][0] = 900


def fall():
    global double_jump, on_box
    canvas.move(player, 0, 5)  # Плавное приземление вниз
    y = canvas.coords(player)[1]
    if y < 422 - 105 - 60 * on_box:  # Если игрок не достиг земли
        canvas.after(10, fall)  # Запуск следующего этапа приземления
    else:
        double_jump = False


def start_game():
    global screen_width, stop, stand_box, on_box, screen_height, canvas, player, background, score, score_label, world_speed, double_jump
    double_jump = False
    stand_box = None
    on_box = False
    stop = False
    # Создаем окно
    window = tk.Tk()
    window.title("Mario")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    canvas = tk.Canvas(window, width=700, height=422)
    window.resizable(False, False)
    canvas.pack()

    world_speed = -1

    # Загружаем фоновое изображение
    background_image = tk.PhotoImage(file="background.png")
    background = canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

    # Создаем игрока
    player_image = tk.PhotoImage(file="player.png")
    player = canvas.create_image(100, 422 - 105, anchor=tk.NW, image=player_image)
    # Отоюражение очков

    score = 0
    score_label = tk.Label(window, text="Score: 0", font=("Arial", 20))
    score_label.place(x=700 / 2, y=10, anchor=tk.CENTER)
    obstacle_image = tk.PhotoImage(file="obstacle.png")
    obstacle = canvas.create_image(300, 422 - 115, anchor=tk.NW, image=obstacle_image)
    obstacles.append([obstacle, [300, 307]])
    obstacle = canvas.create_image(500, 422 - 115, anchor=tk.NW, image=obstacle_image)
    obstacles.append([obstacle, [500, 307]])
    obstacle = canvas.create_image(700, 422 - 115, anchor=tk.NW, image=obstacle_image)
    obstacles.append([obstacle, [700, 307]])
    obstacle = canvas.create_image(900, 422 - 115, anchor=tk.NW, image=obstacle_image)
    obstacles.append([obstacle, [900, 307]])

    # Регистрируем обработчик для прыжка
    window.bind("<space>", lambda event: jump())
    # Запускаем движение фона
    move_background()
    move_obstacles()
    # Запускаем игру
    window.mainloop()
def show_rules():
    messagebox.showinfo("Правила","Вам нужно прыгать по коробкам, нажимая пробел,при ударе о коробку, вы проигрываете")

show_rules()
start_game()


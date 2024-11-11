import tkinter as tk


# Definição das constantes
WIDTH = 1000  # Aumentando a largura
HEIGHT = 800  # Aumentando a altura
PADDLE_WIDTH = 15  # Aumentando a largura das palas
PADDLE_HEIGHT = 150  # Aumentando a altura das palas
BALL_SIZE = 25  # Aumentando o tamanho da bola
BALL_SPEED_X = 8  # Aumentando a velocidade horizontal da bola
BALL_SPEED_Y = 8  # Aumentando a velocidade vertical da bola
PADDLE_SPEED = 30  # Aumentando a velocidade das palas
POINTS_LIMIT = 10  # Limite de pontos para ganhar


class PongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong")


        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()


        self.player1_paddle = self.canvas.create_rectangle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                                           50 + PADDLE_WIDTH, HEIGHT // 2 + PADDLE_HEIGHT // 2,
                                                           fill='white')
        self.player2_paddle = self.canvas.create_rectangle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2,
                                                           WIDTH - 50, HEIGHT // 2 + PADDLE_HEIGHT // 2,
                                                           fill='white')
        self.ball = self.canvas.create_oval(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2,
                                            WIDTH // 2 + BALL_SIZE // 2, HEIGHT // 2 + BALL_SIZE // 2,
                                            fill='white')


        self.ball_x_speed = BALL_SPEED_X
        self.ball_y_speed = BALL_SPEED_Y
        self.player1_score = 0
        self.player2_score = 0


        self.score_display = self.canvas.create_text(WIDTH // 2, 50, text="0 : 0", fill='white', font=('Arial', 36))


        self.root.bind('<w>', self.move_player1_up)
        self.root.bind('<s>', self.move_player1_down)
        self.root.bind('<Up>', self.move_player2_up)
        self.root.bind('<Down>', self.move_player2_down)


        self.update_game()


    def move_player1_up(self, event):
        self.move_paddle(self.player1_paddle, 0, -PADDLE_SPEED)


    def move_player1_down(self, event):
        self.move_paddle(self.player1_paddle, 0, PADDLE_SPEED)


    def move_player2_up(self, event):
        self.move_paddle(self.player2_paddle, 0, -PADDLE_SPEED)


    def move_player2_down(self, event):
        self.move_paddle(self.player2_paddle, 0, PADDLE_SPEED)


    def move_paddle(self, paddle, dx, dy):
        self.canvas.move(paddle, dx, dy)
        self.check_paddle_boundaries(paddle)


    def check_paddle_boundaries(self, paddle):
        x1, y1, x2, y2 = self.canvas.coords(paddle)
        if y1 < 0:
            self.canvas.move(paddle, 0, -y1)
        if y2 > HEIGHT:
            self.canvas.move(paddle, 0, HEIGHT - y2)


    def update_game(self):
        if self.player1_score >= POINTS_LIMIT or self.player2_score >= POINTS_LIMIT:
            self.show_winner()
        else:
            self.move_ball()
            self.check_collisions()
            self.update_score()
            self.root.after(20, self.update_game)


    def move_ball(self):
        self.canvas.move(self.ball, self.ball_x_speed, self.ball_y_speed)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)


        if y1 <= 0 or y2 >= HEIGHT:
            self.ball_y_speed = -self.ball_y_speed


        if x1 <= 0:
            self.player2_score += 1
            self.reset_ball()


        if x2 >= WIDTH:
            self.player1_score += 1
            self.reset_ball()


    def check_collisions(self):
        ball_coords = self.canvas.coords(self.ball)
        paddle1_coords = self.canvas.coords(self.player1_paddle)
        paddle2_coords = self.canvas.coords(self.player2_paddle)


        if self.check_collision(ball_coords, paddle1_coords) or self.check_collision(ball_coords, paddle2_coords):
            self.ball_x_speed = -self.ball_x_speed


    def check_collision(self, ball_coords, paddle_coords):
        bx1, by1, bx2, by2 = ball_coords
        px1, py1, px2, py2 = paddle_coords


        return bx2 >= px1 and bx1 <= px2 and by2 >= py1 and by1 <= py2


    def reset_ball(self):
        self.canvas.coords(self.ball, WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2,
                                         WIDTH // 2 + BALL_SIZE // 2, HEIGHT // 2 + BALL_SIZE // 2)
        self.ball_x_speed = BALL_SPEED_X
        self.ball_y_speed = BALL_SPEED_Y


    def update_score(self):
        self.canvas.itemconfig(self.score_display, text=f"{self.player1_score} : {self.player2_score}")


    def show_winner(self):
        winner = "Jogador 1 ganhou!" if self.player1_score >= POINTS_LIMIT else "Jogador 2 ganhou!"
        self.canvas.delete("all")  # Remove all existing elements
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=winner, fill='white', font=('Arial', 48))
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()

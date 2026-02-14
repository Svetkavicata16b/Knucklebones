import tkinter as tk
import random
import time
import copy


class View:
    def __init__(self):
        self.screen = tk.Tk()
        self.screen.title("Knucklebones")

        self.empty_img = tk.PhotoImage(file="images/empty.png").zoom(5)
        self.dice_1_img = tk.PhotoImage(file="images/dice_1.png").zoom(5)
        self.dice_2_img = tk.PhotoImage(file="images/dice_2.png").zoom(5)
        self.dice_3_img = tk.PhotoImage(file="images/dice_3.png").zoom(5)
        self.dice_4_img = tk.PhotoImage(file="images/dice_4.png").zoom(5)
        self.dice_5_img = tk.PhotoImage(file="images/dice_5.png").zoom(5)
        self.dice_6_img = tk.PhotoImage(file="images/dice_6.png").zoom(5)

        self.dice_1_blue_img = tk.PhotoImage(file="images/dice_1_blue.png").zoom(5)
        self.dice_2_blue_img = tk.PhotoImage(file="images/dice_2_blue.png").zoom(5)
        self.dice_3_blue_img = tk.PhotoImage(file="images/dice_3_blue.png").zoom(5)

        self.dice_images = {
            0: self.empty_img,
            1: self.dice_1_img,
            2: self.dice_2_img,
            3: self.dice_3_img,
            4: self.dice_4_img,
            5: self.dice_5_img,
            6: self.dice_6_img
        }

        self.screen.iconphoto(True, self.dice_6_img)

        self.screen_frame = tk.Frame(self.screen)
        self.game_frame = tk.Frame(self.screen_frame)

        self.score_frame = tk.Frame(self.screen_frame)
        self.score_label = tk.Label(self.score_frame, text="Computer - Player\n0 - 0", font=("Courier New", 30))

        self.rolled_dice_frame = tk.Frame(self.game_frame)
        self.rolled_dice_label = tk.Label(self.rolled_dice_frame, image=self.dice_images[0])

        self.table_frame = tk.Frame(self.game_frame)

        self.row_of_columns_frame = tk.Frame(self.table_frame)
        tk.Label(self.row_of_columns_frame, image=self.dice_1_blue_img).pack(side="left", padx=5, pady=5)
        tk.Label(self.row_of_columns_frame, image=self.dice_2_blue_img).pack(side="left", padx=5, pady=5)
        tk.Label(self.row_of_columns_frame, image=self.dice_3_blue_img).pack(side="left", padx=5, pady=5)

        self.enemy_frame = tk.Frame(self.table_frame)
        self.enemy_frame_column_0 = tk.Frame(self.enemy_frame)
        self.enemy_frame_column_1 = tk.Frame(self.enemy_frame)
        self.enemy_frame_column_2 = tk.Frame(self.enemy_frame)

        self.player_frame = tk.Frame(self.table_frame)
        self.player_frame_column_0 = tk.Frame(self.player_frame)
        self.player_frame_column_1 = tk.Frame(self.player_frame)
        self.player_frame_column_2 = tk.Frame(self.player_frame)

        self.enemy_table = [self.enemy_frame_column_0, self.enemy_frame_column_1, self.enemy_frame_column_2]
        self.player_table = [self.player_frame_column_0, self.player_frame_column_1, self.player_frame_column_2]
        self.table = [self.enemy_table, self.player_table]

        self.score_label.pack()
        self.score_frame.pack()

        self.rolled_dice_label.pack()
        self.rolled_dice_frame.pack(side="left", padx=15, pady=15)

        self.table_frame.pack(side="left")

        self.enemy_frame.pack()
        self.enemy_frame_column_0.pack(side="left", padx=5, pady=5)
        self.enemy_frame_column_1.pack(side="left", padx=5, pady=5)
        self.enemy_frame_column_2.pack(side="left", padx=5, pady=5)

        self.row_of_columns_frame.pack()

        self.player_frame.pack()
        self.player_frame_column_0.pack(side="left", padx=5, pady=5)
        self.player_frame_column_1.pack(side="left", padx=5, pady=5)
        self.player_frame_column_2.pack(side="left", padx=5, pady=5)

        self.game_frame.pack(expand=True)
        self.screen_frame.pack(expand=True)

        self.change_table([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]])

    def change_score(self, enemy_score, player_score):
        self.score_label["text"] = f"Computer - Player\n{enemy_score} - {player_score}"

    def change_score_at_win(self, current_turn):
        self.score_label["text"] = f"{['Computer', 'Player'][current_turn]} won!\n" + self.score_label["text"]

    def change_table(self, table):
        for l in range(2):
            for i in range(3):
                for widget in self.table[l][i].winfo_children():
                    widget.destroy()

                j_range = None

                if l:
                    j_range = range(3)
                else:
                    j_range = range(2, -1, -1)

                for j in j_range:
                    if len(table[l][i]) > j:
                        tk.Label(self.table[l][i], image=self.dice_images[table[l][i][j]]).pack()
                    else:
                        tk.Label(self.table[l][i], image=self.dice_images[0]).pack()

    def change_rolled_dice(self, rolled_dice):
        self.rolled_dice_label["image"] = self.dice_images[rolled_dice]


class Model:
    def __init__(self):
        self.table = [[[], [], []], [[], [], []]]
        self.player_score = 0
        self.enemy_score = 0
        self.player_dices = 0
        self.enemy_dices = 0

    def add_dice(self, table, current_turn, current_dice_number, current_column):
        if len(table[current_turn][current_column]) == 3:
            return None

        table[current_turn][current_column].append(current_dice_number)

        current_dice_number_remove_count = 0

        for i in range(len(table[(current_turn + 1) % 2][current_column]) - 1, -1, -1):
            if table[(current_turn + 1) % 2][current_column][i] == current_dice_number:
                table[(current_turn + 1) % 2][current_column].pop(i)
                current_dice_number_remove_count += 1

        current_dice_number_count = 0

        for i in range(len(table[current_turn][current_column])):
            if table[current_turn][current_column][i] == current_dice_number:
                current_dice_number_count += 1

        return [table, (current_dice_number_count * current_dice_number_count - (current_dice_number_count - 1) * (current_dice_number_count - 1)) * current_dice_number, current_dice_number_remove_count * current_dice_number_remove_count * current_dice_number, len(table[current_turn][current_column]), current_dice_number_remove_count]

    def process_enemy_turn(self, current_dice_number):
        best_return_list = [[[[], [], []], [[], [], []]], -1000, -1000, 3, 0]

        for i in range(0, 3):
            if len(self.table[0][i]) < 3:
                current_return_list = self.add_dice(copy.deepcopy(self.table), 0, current_dice_number, i)

                if current_return_list[1] + current_return_list[2] - [0, 4, 8][current_return_list[3] - 1] > best_return_list[1] + best_return_list[2] - [0, 4, 8][best_return_list[3] - 1]:
                    best_return_list = current_return_list

        if best_return_list != [[[[], [], []], [[], [], []]], -1000, -1000, 3, 0]:
            self.player_score -= best_return_list[2]
            self.enemy_score += best_return_list[1]
            self.table = best_return_list[0]
            self.enemy_dices += 1
            self.player_dices -= best_return_list[4]

    def process_player_turn(self, current_dice_number, current_column):
        return_list = self.add_dice(self.table, 1, current_dice_number, current_column)

        if return_list:
            self.player_score += return_list[1]
            self.enemy_score -= return_list[2]
            self.table = return_list[0]
            self.player_dices += 1
            self.enemy_dices -= return_list[4]

class Controller:
    def __init__(self):
        self.view = View()
        self.model = Model()
        self.rolled_dice_number = 0

    def main(self):
        time.sleep(0.5)

        if self.model.player_dices == 9:
            self.end_of_game(self.model.enemy_score < self.model.player_score)
            return None

        self.roll_dice()
        time.sleep(0.5)
        self.enemy_turn()
        time.sleep(0.5)

        if self.model.enemy_dices == 9:
            self.end_of_game(self.model.enemy_score < self.model.player_score)
            return None

        self.roll_dice()
        time.sleep(0.5)
        self.player_turn()

    def roll_dice(self):
        for i in range(6):
            rolling_dice = random.randint(1, 6)
            time.sleep(i * i / 100)
            self.view.change_rolled_dice(rolling_dice)
            self.rolled_dice_number = rolling_dice
            self.view.screen.update()

    def enemy_turn(self):
        self.model.process_enemy_turn(self.rolled_dice_number)
        self.update_screen()

    def player_turn(self):
        self.view.screen.bind("1", self.one_is_pressed)
        self.view.screen.bind("2", self.two_is_pressed)
        self.view.screen.bind("3", self.three_is_pressed)

    def one_is_pressed(self, event):
        if len(self.model.table[1][0]) == 3:
            self.player_turn()
        else:
            self.view.screen.unbind("1")
            self.view.screen.unbind("2")
            self.view.screen.unbind("3")

            self.model.process_player_turn(self.rolled_dice_number, 0)
            self.update_screen()
            self.view.screen.after(0, self.main)

    def two_is_pressed(self, event):
        if len(self.model.table[1][1]) == 3:
            self.player_turn()
        else:
            self.view.screen.unbind("1")
            self.view.screen.unbind("2")
            self.view.screen.unbind("3")

            self.model.process_player_turn(self.rolled_dice_number, 1)
            self.update_screen()
            self.view.screen.after(0, self.main)

    def three_is_pressed(self, event):
        if len(self.model.table[1][2]) == 3:
            self.player_turn()
        else:
            self.view.screen.unbind("1")
            self.view.screen.unbind("2")
            self.view.screen.unbind("3")

            self.model.process_player_turn(self.rolled_dice_number, 2)
            self.update_screen()
            self.view.screen.after(0, self.main)

    def update_screen(self):
        self.view.change_score(self.model.enemy_score, self.model.player_score)
        self.view.change_table(self.model.table)
        self.view.change_rolled_dice(self.rolled_dice_number)
        self.view.screen.update()

    def end_of_game(self, current_turn):
        self.view.change_score_at_win(current_turn)

        self.view.screen.bind("<Return>", self.new_game)

    def new_game(self, event):
        self.view.screen.unbind("<Return>")
        self.model.table = [[[], [], []], [[], [], []]]
        self.model.player_score = 0
        self.model.enemy_score = 0
        self.model.player_dices = 0
        self.model.enemy_dices = 0
        self.rolled_dice_number = 0
        self.update_screen()
        self.view.screen.after(0, self.main)



if __name__ == '__main__':
    controller = Controller()
    controller.main()
    controller.view.screen.mainloop()

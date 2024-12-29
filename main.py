import random
from monster import Monster
from typewriter import typewriter
from settings import settings

class Game:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        settings.reset()
        self.remaining_torches = settings.DEFAULT_NUM_OF_TORCHES
        self.searched_positions = settings.DEFAULT_SEARCHED_POSITIONS
        self.player_position = settings.DEFAULT_PLAYER_POS
        self.treasure_position = settings.DEFAULT_TREASURE_POS
        self.monster = Monster(settings.DEFAULT_MONSTER_POS)

    def treasure_found(self):
        return self.player_position == self.treasure_position

    def draw_map(self, show_treasure=False):
        grid = [['□ ' for _ in range(settings.GRID_WIDTH)] for _ in range(settings.GRID_HEIGHT)]
        for pos in self.searched_positions:
            x, y = pos
            grid[y][x] = '\033[96mX \033[0m'
        player_x, player_y = self.player_position
        grid[player_y][player_x] = '\033[92m⧆ \033[0m'
        monster_x, monster_y = self.monster.position
        grid[monster_y][monster_x] = '\033[95mM \033[0m'
        if show_treasure:
            treasure_x, treasure_y = self.treasure_position
            grid[treasure_y][treasure_x] = '\033[93m⚿ \033[0m'
        for row in grid:
            print(''.join(row))

    def light_torch(self):
        if self.remaining_torches > 0:
            self.remaining_torches -= 1
            typewriter("You light a torch and check your map.", 0.05)
            print(" ")
            self.draw_map()
            print(" ")
            typewriter("\033[92m⧆\033[0m: Your current location.", 0.05)
            typewriter("\033[96mX\033[0m: Spots you've already dug.", 0.05)
            typewriter("\033[95mM\033[0m: You see an ominous shadowy figure standing there...", 0.1)
            if self.remaining_torches == 1:
                typewriter(f"The light has gone out. You have {self.remaining_torches} torch left", 0.05)
            else:
                typewriter(f"The light has gone out. You have {self.remaining_torches} torches left", 0.05)
            print(" ")
        else:
            typewriter("You don't have any torches left", 0.05)

    def sweep_for_treasure(self):
        player_x, player_y = self.player_position
        treasure_x, treasure_y = self.treasure_position
        distance = abs(player_x - treasure_x) + abs(player_y - treasure_y)
        if distance == 0:
            typewriter("The metal detector is going wild!!", 0.05)
        elif distance == 1:
            typewriter("The metal detector is beeping rapidly!", 0.05)
        elif distance == 2:
            typewriter("The metal detector is slowly beeping.", 0.05)
        else:
            typewriter("The metal detector is silent.", 0.05)

    def display_commands(self):
        print(" ")
        typewriter("*****************", 0.02)
        typewriter("* Legal commands *", 0.02)
        typewriter("*****************", 0.02)
        print(" ")
        typewriter("GO NORTH", 0.02)
        typewriter("GO SOUTH", 0.02)
        typewriter("GO EAST", 0.02)
        typewriter("GO WEST", 0.02)
        typewriter("DIG", 0.02)
        typewriter("LIGHT TORCH: check your map", 0.02)
        typewriter("SWEEP: use metal detector", 0.02)
        typewriter("HELP: displays these commands again (the monster will not move)", 0.02)
        print(" ")

    def debug(self):
        print(" ")
        self.draw_map(show_treasure=True)
        print(" ")

    def welcome_screen(self):
        response = input(
            "Welcome to Frankie's text based adventure game. Have you played this game before? (Y/N): "
        ).strip().lower()
        if response in ['n', 'no']:
            print(" ")
            typewriter("Here are the rules:", 0.05)
            typewriter("You are in a dark cave. Each turn you can use a command to do one of the following.", 0.05)
            typewriter("- Move north, south, east or west", 0.05)
            typewriter("- Use a metal detector.", 0.05)
            typewriter("- Dig for treasure.", 0.05)
            typewriter("- Light a torch and check your map. You only get 3 torches.", 0.05)
            typewriter("Beware, there is a monster in the cave with you. Each turn the monster moves one pace.", 0.05)
            typewriter("The game will end if you find the treasure... or the monster catches you. Good luck!", 0.05)
            print(" ")
            self.display_commands()

    def play_again(self):
        response = input("Do you want to play again? (Y/N): ").strip().lower()
        return response in ["y", "yes"]

    def main_loop(self):
        self.welcome_screen()
        while True:
            print(" ")
            command = input("What do you want to do?: ").strip().lower()
            monster_should_move = True

            match command:
                case "go north":
                    if self.player_position[1] > 0:
                        self.player_position = (self.player_position[0], self.player_position[1] - 1)
                        typewriter("You moved north.", 0.05)
                    else:
                        typewriter("The way is blocked.", 0.05)

                case "go south":
                    if self.player_position[1] < settings.GRID_HEIGHT - 1:
                        self.player_position = (self.player_position[0], self.player_position[1] + 1)
                        typewriter("You moved south.", 0.05)
                    else:
                        typewriter("The way is blocked.", 0.05)

                case "go east":
                    if self.player_position[0] < settings.GRID_WIDTH - 1:
                        self.player_position = (self.player_position[0] + 1, self.player_position[1])
                        typewriter("You moved east.", 0.05)
                    else:
                        typewriter("The way is blocked.", 0.05)

                case "go west":
                    if self.player_position[0] > 0:
                        self.player_position = (self.player_position[0] - 1, self.player_position[1])
                        typewriter("You moved west.", 0.05)
                    else:
                        typewriter("The way is blocked.", 0.05)

                case "dig":
                    if self.treasure_found():
                        typewriter("Congratulations! You found the treasure!", 0.05)
                        print(" ")
                        if self.play_again():
                            self.reset_game()
                            continue
                        else:
                            typewriter("Thank you for playing!", 0.05)
                            break
                    else:
                        typewriter("There is nothing here.", 0.05)
                        self.searched_positions.append(self.player_position)

                case "light torch":
                    self.light_torch()

                case "sweep":
                    self.sweep_for_treasure()

                case "help":
                    self.display_commands()
                    monster_should_move = False

                case "cheat":
                    print(" ")
                    self.debug()
                    monster_should_move = False

                case _:
                    typewriter(f"I don't know what '{command}' means.", 0.05)
                    print(" ")
                    monster_should_move = False

            if monster_should_move:
                self.monster.move(self.player_position)
                if self.monster.check_if_caught(self.player_position):
                    print(" ")
                    typewriter(f"You were caught by the monster!", 0.05)
                    print(" ")
                    if self.play_again():
                        self.reset_game()
                        continue
                    else:
                        typewriter("Thank you for playing!", 0.05)
                        break

        print(" ")
        typewriter("GAME OVER", 0.5)

if __name__ == '__main__':
    game = Game()
    game.main_loop()
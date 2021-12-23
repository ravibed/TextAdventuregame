import enemies
import npc
import random


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return """
        Welcome,Ruby home's.....
        """


class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.Woodpecker()
            self.alive_text = "Woodpeckers jump from their webs directly in front of you. " 
            self.dead_text = """The corpse of a dead woodpecker 
                             Woodpecker on the ground."""
        elif r < 0.80:
            self.enemy = enemies.Storkpecker()
            self.alive_text = "An Storkpecker is blocking your path!"
            self.dead_text = "A dead Storkpecker."\
                             " you of your win!!!"
        elif r < 0.95:
            self.enemy = enemies.Pangolin()
            self.alive_text ="Pangolin jump from their webs directly in front of you." 
            self.dead_text = "Pangolin of dead bats are scattered on the ground."
        else:
            self.enemy = enemies.Foxfire()
            self.alive_text = "You've disturbed a rock Foxfire " \
                              "from his slumber!"
            self.dead_text = "A dead focfire " \
                             "into an ordinary rock."

        super().__init__(x, y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.health = player.health - self.enemy.damage
            print("Enemy does {} damage. You have {} Health remaining.".
                  format(self.enemy.damage, player.health))


class VictoryTile(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... ...  It's is sunlight


        Victory is yours!
        """


class FindCoinTile(MapTile):
    def __init__(self, x, y):
        self.Coin = random.randint(1, 50)
        self.Coin_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.Coin_claimed:
            self.coin_claimed = True
            player.coin = player.coin + self.Coin
            print("+{} coin added.".format(self.Coin))

    def intro_text(self):
        if self.Coin_claimed:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
        else:
            return """
            Someone dropped some coin. You pick it up.
            """


class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit?")
            user_input = input()
            if user_input in ['Q', 'q']:
                return
            elif user_input in ['B', 'b']:
                print("Here's whats available to buy: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['S', 's']:
                print("Here's whats available to sell: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice!")

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Coin".format(i, item.name, item.value))
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("Invalid choice!")

    def swap(self, seller, buyer, item):
        if item.value > buyer.Coin:
            print("That's too expensive")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.coin = seller.coin + item.value
        buyer.coin = buyer.coin - item.value
        print("Trade complete!")


    def intro_text(self):
        return """
        A frail not-quite-human, not-quite-creature squats in the corner
        clinking his coin coins together. He looks willing to trade.
        """

world_dsl = """
|ET|ET|VT|ET|ET|
|ET|  |  |  |ET|
|ET|FG|ET|  |TT|
|TT|  |ST|FG|ET|
|FG|  |ET|  |FG|
"""


def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True

tile_type_dict = {"VT": VictoryTile,
                  "ET": EnemyTile,
                  "ST": StartTile,
                  "FG": FindCoinTile,
                  "TT": TraderTile,
                  "  ": None}


world_map = []

start_tile_location = None

def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)


def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None

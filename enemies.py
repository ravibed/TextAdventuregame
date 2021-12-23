class Enemy:
    def __init__(self):
        raise NotImplementedError("Do not create raw Enemy objects.")

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.health > 0


class Woodpecker(Enemy):
    def __init__(self):
        self.name = "Woodpecker"
        self.health = 10
        self.damage = 2


class Storkpecker(Enemy):
    def __init__(self):
        self.name = "Storkpecker"
        self.health = 30
        self.damage = 10


class Pangolin(Enemy):
    def __init__(self):
        self.name = "Pangolin"
        self.health = 100
        self.damage = 4


class Foxfire(Enemy):
    def __init__(self):
        self.name = "Foxfire"
        self.health = 80
        self.damage = 15

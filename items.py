class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create raw Weapon objects.")

    def __str__(self):
        return self.name


class Rock(Weapon):
    def __init__(self):
        self.name = "Rock"
        self.description = "The size of a fist, good for bludgeoning."
        self.damage = 5
        self.value = 1


class Dagger(Weapon):
    def __init__(self):
        self.name = "Dagger"
        self.description = "Rusted small dagger. " \
                           "Almost as dangerous as a rock."
        self.damage = 5
        self.value = 10


class RustySword(Weapon):
    def __init__(self):
        self.name = "Rusty sword"
        self.description = "The sword shows its age, " \
                           "but still has some fight in it."
        self.damage = 10
        self.value = 80


class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")

    def __str__(self):
        return "{} (+{} Health)".format(self.name, self.healing_value)


class CrustyBread(Consumable):
    def __init__(self):
        self.name = "Crusty Bread"
        self.healing_value = 15
        self.value = 10

class HealingPotion(Consumable):
    def __init__(self):
        self.name = "Healing Potion"
        self.healing_value = 40
        self.value = 50

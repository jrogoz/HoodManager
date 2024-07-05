import enum


class Hair(enum.Enum):
    BLACK = 1
    BROWN = 2
    BLONDE = 3
    RED = 4


class Eyes(enum.Enum):
    BROWN = 1
    DARK_BLUE = 2
    GREEN = 3
    LIGHT_BLUE = 4
    GREY = 5
    ALIEN = 6


class Skin(enum.Enum):
    LIGHT = 1
    TAN = 2
    MEDIUM = 3
    DARK = 4
    GREEN = 5
    WHITE = 6
    ZOMBIE = 7


class Race(enum.Enum):
    HUMAN = 1
    ALIEN = 2
    ZOMBIE = 3
    VAMPIRE = 4
    WEREWOLF = 5
    PLANTSIM = 6
    WITCH = 7


class LifeStage(enum.Enum):
    BABY = 1
    TODDLER = 2
    CHILD = 3
    TEENAGER = 4
    YOUNG_ADULT = 5
    ADULT = 6
    ELDER = 7


class SexualOrient(enum.Enum):
    NOT_SPECIFIED = 1
    STRAIGHT = 2
    GAY = 3
    BISEXUAL = 4

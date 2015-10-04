class GameObject:
    """ A general game object with x and y coordinates representing its location on the gameboard.

    Attributes:
        x (int): Represents the x-coordinate on the gameboard.
        y (int): Represents the y-coordinate on the gameboard.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PowerUp(GameObject):
    """ A general object representing power-ups with x and y coordinates representing its location on the gameboard.

    Inherits from GameObject.

    Attributes:
        power_up_type (Enum): The type of power-up as either SHIELD, LASER, or TELEPORT .
    """
    def __init__(self, x, y, power_up_type):
        super().__init__(x, y)
        self.power_up_type = power_up_type


class Turret(GameObject):
    """ An object representing a turret on the gameboard.

    A turret fires for fire_time consecutive turns and is inactive for cooldown_time turns.

    Inherits from GameObject.

    Attributes:
        is_firing_next_turn (boolean): True iff this turret is firing the next turn.
        is_dead (boolean): True iff this turret has been destroyed and is no longer active.
        did_fire (boolean): True iff this turret fired in the last turn.
        fire_time (int): The number of consecutive turns the turret will fire.
        cooldown_time (int): The number of consecutive turns the turret will not fire.
    """
    def __init__(self, x, y, is_firing_next_turn, is_dead, did_fire, fire_time, cooldown_time):
        super().__init__(x, y)
        self.is_firing_next_turn = is_firing_next_turn
        self.is_dead = is_dead
        self.did_fire = did_fire
        self.fire_time = fire_time
        self.cooldown_time = cooldown_time


class Wall(GameObject):
    """ An object representing a wall and its location on the gameboard.

    Inherits from GameObject.
    """
    def __init__(self, x, y):
        super().__init__(x, y)


class DirectionalGameObject(GameObject):
    """ An object representing any GameObject with a direction.

    Inherits from GameObject.

    Attributes:
        direction (Enum): The direction the object is facing as either UP, DOWN, LEFT, RIGHT.
    """
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.direction = direction


class Bullet(DirectionalGameObject):
    """ An object representing a bullet on the gameboard.

    Attributes:
        shooter (Combatant): A reference to the Combatant that fired the bullet.
    """
    def __init__(self, x, y, direction, shooter):
        super().__init__(x, y, direction)
        self.shooter = shooter


class Combatant(DirectionalGameObject):
    """ A general object representing a player on the gameboard.

    Attributes:
        score (int): This Combatant's current score.
        hp (int): This Combatant's current hp (remaining lives/hit points).
        shield_active (boolean): True iff this Combatant's shield is currently active.
        laser_count (int): The number of laser power-ups this Combatant has.
        teleport_count (int): The number of teleport power-ups this Combatant has.
        shield_count (int): The number of shield power-ups this Combatant has.
    """
    def __init__(self, x, y, direction, score, hp, shield_active, laser_count, teleport_count, shield_count):
        super().__init__(x, y, direction)
        self.score = score
        self.hp = hp
        self.shield_active = shield_active
        self.laser_count = laser_count
        self.teleport_count = teleport_count
        self.shield_count = shield_count


class Opponent(Combatant):
    """ An object representing a player's Opponent in the game.

    Inherits from Combatant.

    Attributes:
        last_move (Enum) = The last move this Opponent made. All possible moves are listed in Move in Enums.py.
    """

    def __init__(self, x, y, direction, score, hp, shield_active, last_move, laser_count, teleport_count, shield_count):
        super().__init__(x, y, direction, score, hp, shield_active, laser_count, teleport_count, shield_count)
        self.last_move = last_move


class Player(Combatant):
    """ An object representing the player (you) on the gameboard.

    Inherits from Combatant.

    Attributes:
        projectiles (List[Enum]): A list of projectiles this Player was hit by, either a LASER or BULLET.
        shooters (List[Combatant]): A list of Combatants that fired the projectiles in projectiles. Each index contains
                                    a reference to the combatant that fired it or None (where a Turret fired that projectile).
                                    This list is the same length as projectiles and the indices are mapped such that
                                    projectiles[x] was fired by shooters[x], where x an index.
        did_make_a_move (boolean): True iff this Player made a valid move last turn.
    """
    def __init__(self, x, y, direction, score, hp, laser_count, teleport_count, shield_count, did_make_a_move,
                 projectiles,
                 shooters, shield_active):
        super().__init__(x, y, direction, score, hp, shield_active, laser_count, teleport_count, shield_count)
        self.projectiles = projectiles
        self.shooters = shooters
        self.did_make_a_move = did_make_a_move

    def was_hit(self):
        if (len(self.projectiles) > 0):
            return True
        else:
            return False

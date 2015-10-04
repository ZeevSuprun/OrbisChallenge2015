from PythonClientAPI.libs.Game.MapOutOfBoundsException import *


class Gameboard:
    """ The current state of the gameboard along with information about the game state

    Attributes:
        width (int): The width of the map i.e number of tiles width-wise.
        height (int): The height of the map i.e number of tiles height-wise.
        current_turn (int): The current turn in the game.
        max_turn (int): The maximum number of turns in the game.

        bullets (List[bullet]): A list of all the bullet objects in the game.
        power_ups (List[power_ups]): A list of all the power_up objects in the game.
        turrets (List[turret]): A list of all the turret objects in the game.
        walls (List[wall]): A list of all the wall objects in the game.

        teleport_locations (List[List[x, y]): A list of all the teleport locations in the game, each one being a list
                                              of two items, with the first being the x coordinate and the second being
                                              a y coordinate.
        game_board_objects(List[Object]): A list of every game object in the game.

        bullets_at_tile(List[List[List[Bullet]]]: A 2D-array of all bullets on each tile, with x and y coordinates mapped
                                                  to the first and second list accordingly.
                                                  i.e bullets_at_tile[2][3] returns a list of all bullets on the tile
                                                  located at (x, y) coordinates (2, 3).
        power_up_at_tile(List[List[List[PowerUps]]]: A 2D-array of all power_ups on each tile, with x and y coordinates mapped
                                                  to the first and second list accordingly.
                                                  i.e power_up_at_tile[2][3] returns a list of all power_ups on the tile
                                                  located at (x, y) coordinates (2, 3).
        wall_at_tile(List[List[Wall]]: A 2D-array of all walls on each tile, with x and y coordinates mapped
                                                  to the first and second list accordingly.
                                                  i.e wall_at_tile[2][3] returns the wall on the tile (if it exists)
                                                  located at (x, y) coordinates (2, 3).
        turret_at_tile(List[List[Turret]]: A 2D-array of all bullets on each tile, with x and y coordinates mapped
                                                  to the first and second list accordingly.
                                                  i.e turret_at_tile[2][3] returns a turret on the tile (if it exists)
                                                  located at (x, y) coordinates (2, 3).







    """
    def __init__(self, width, height, current_turn, max_turn):
        self.width = width
        self.height = height
        self.current_turn = current_turn
        self.max_turn = max_turn
        self.bullets = []
        self.power_ups = []
        self.turrets = []
        self.walls = []
        self.teleport_locations = []
        self.game_board_objects = [[[] for x in range(height)] for x in range(width)]
        self.bullets_at_tile = [[[] for x in range(height)] for x in range(width)]
        self.power_up_at_tile = [[None for x in range(height)] for x in range(width)]
        self.wall_at_tile = [[None for x in range(height)] for x in range(width)]
        self.turret_at_tile = [[None for x in range(height)] for x in range(width)]

    def get_game_objects_at_tile(self, x, y):
        ''' (int, int) ->

        '''
        return self.game_board_objects[x][y]

    def get_turns_remaining(self):
        """ Return the number of turns remaining in this game.

        Calculates and returns the number of turns remaining in game based off
        of the gameboard's current turn and max turns in this game.
        Args:
            self: The gameboard.

        Returns:
            An integer representing the number of turns remaining in a game.
        """
        return self.max_turn - self.current_turn

    def are_bullets_at_tile(self, x, y):
        """ Return True iff bullets exist on the tile at position (x, y).

        Args:
            self: The Gameboard.
            x: The x-coordinate on the gameboard.
            y: The y-coordinate on the gameboard.

        Returns:
            A boolean value indicating whether or not any bullets exist at the given x and y
            coordinates on the gameboard.

        Raises:
            MapOufOfBoundsError: An error occurred when trying to check for a bullet at x and y
            coordinates beyond the boundaries of the map.

        """
        if self.verify_x_y_beyond_map(x, y):
            raise MapOutOfBoundsException("Cannot access bullets outside of map boundaries.")
        else:
            return self.bullets_at_tile[x][y]

    def is_turret_at_tile(self, x, y):
        """ Return True iff a turret exists on the tile at position (x, y).

        Args:
            self: The Gameboard.
            x: The x-coordinate on the gameboard.
            y: The y-coordinate on the gameboard.

        Returns:
            A boolean value indicating whether or not a turret exists at the given x and y
            coordinates on the gameboard.

        Raises:
            MapOufOfBoundsError: An error occurred when trying to check for a turret at x and y
            coordinates beyond the boundaries of the map.

        """
        if self.verify_x_y_beyond_map(x, y):
            raise MapOutOfBoundsException("Cannot access turrets outside of map boundaries.")
        else:
            return self.turret_at_tile[x][y] is not None

    def is_power_up_at_tile(self, x, y):
        """ Return True iff a powerup exists on the tile at position (x, y).

        Args:
            self: The Gameboard.
            x: The x-coordinate on the gameboard.
            y: The y-coordinate on the gameboard.

        Returns:
            A boolean value indicating whether or not a powerup exists at the given x and y
            coordinates on the gameboard.

        Raises:
            MapOufOfBoundsError: An error occurred when trying to check for a powerup at x and y
            coordinates beyond the boundaries of the map.

        """
        if self.verify_x_y_beyond_map(x, y):
            raise MapOutOfBoundsException("Cannot access powerups outside of map boundaries.")
        else:
            return self.power_up_at_tile[x][y] is not None

    def is_wall_at_tile(self, x, y):
        """ Return True iff a wall exists on the tile at position (x, y).

        Args:
            self: The Gameboard.
            x: The x-coordinate on the gameboard.
            y: The y-coordinate on the gameboard.

        Returns:
            A boolean value indicating whether or not a wall exists at the given x and y
            coordinates on the gameboard.

        Raises:
            MapOufOfBoundsError: An error occurred when trying to check for a wall at x and y
            coordinates beyond the boundaries of the map.

        """
        if self.verify_x_y_beyond_map(x, y):
            raise MapOutOfBoundsException("Cannot access walls outside of map boundaries.")
        else:
            return self.wall_at_tile[x][y] is not None

    def verify_x_y_beyond_map(self, x, y):
        return (x < 0) or (x > self.width - 1) or (y < 0) or (y > self.height - 1)

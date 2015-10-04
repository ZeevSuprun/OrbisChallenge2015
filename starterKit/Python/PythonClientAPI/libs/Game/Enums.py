from enum import Enum

Direction = Enum('Direction', 'UP DOWN LEFT RIGHT')
Move = Enum('Move',
            'FACE_UP FACE_DOWN FACE_LEFT FACE_RIGHT NONE SHOOT FORWARD SHIELD LASER TELEPORT_0 TELEPORT_1 TELEPORT_2 TELEPORT_3 TELEPORT_4 TELEPORT_5')

ProjectileTypes = Enum('ProjectileTypes', 'BULLET LASER')

PowerUpTypes = Enum('PowerUpType', 'SHIELD LASER TELEPORT')

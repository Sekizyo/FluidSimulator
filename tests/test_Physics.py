from modules.physics import Physics
from modules.ball import Ball

def test_gravity():
    ball = Ball()
    physics = Physics()

    physics.gravity(ball)

    pass

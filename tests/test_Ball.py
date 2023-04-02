import pytest
from modules import WIDTH, HEIGHT
from modules.ball import Ball

def test_moveTo():
    ball = Ball()
    ball.moveTo(10,10)
    assert ball.x == 10
    assert ball.y == 10

def test_setDirection():
    ball = Ball()
    ball.setDirection(80)

    assert ball.direction == 80

def test_setDirectionNoParameters():
    ball = Ball()
    ball.setDirection()

    assert ball.direction == 0

def test_setDirectionOver360():
    ball = Ball()
    ball.setDirection(370)

    assert ball.direction == 10

def test_setDirectionNegative():
    ball = Ball()
    ball.setDirection(-10)

    assert ball.direction == 0

def test_changeSpeed():
    ball = Ball()
    ball.changeSpeed(10)
    assert ball.speed == 10

def test_changeSpeedNoParameters():
    ball = Ball()
    ball.changeSpeed()
    assert ball.speed == 0

def test_changeSpeedOverLimit():
    ball = Ball()
    ball.changeSpeed(350)
    assert ball.speed == 250

def test_changeSpeedNegativeValue():
    ball = Ball()
    ball.changeSpeed(-10)
    assert ball.speed == 0

def test_moveToBeyondScreenSize():
    ball = Ball()
    ball.moveTo(WIDTH+1, HEIGHT+1)
    assert ball.x == WIDTH
    assert ball.y == HEIGHT

def test_moveToUnderScreenSize():
    ball = Ball()
    ball.moveTo(-1, -1)
    assert ball.x == 0
    assert ball.y == 0


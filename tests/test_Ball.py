import pytest
from modules import WIDTH, HEIGHT
from modules.ball import Ball

def test_moveTo():
    ball = Ball()
    ball.moveTo(10,10)
    assert ball.x == 10
    assert ball.y == 10

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


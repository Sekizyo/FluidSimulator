import pytest 
from modules.ball import Balls

def test_createBall():
    balls = Balls()
    balls.createBall()
    
    assert len(balls.balls) == 1
    assert balls.ballCount == 1

def test_createBalls():
    balls = Balls()
    balls.createBalls(5)
    
    assert len(balls.balls) == 5
    assert balls.ballCount == 5

def test_clearBalls():
    balls = Balls()
    balls.createBall()
    balls.clearBalls()

    assert len(balls.balls) == 0
    assert balls.ballCount == 0

def test_createBallsNoArgument():
    balls = Balls()
    balls.createBalls()
    
    assert len(balls.balls) == 1
    assert balls.ballCount == 1

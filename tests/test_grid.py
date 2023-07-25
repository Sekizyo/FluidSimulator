import pytest 

def test_fps():
    from modules.game import Game
    game = Game(testRun=True)
    avgFps = game.run()

    assert avgFps > 30

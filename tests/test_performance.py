import psutil
from modules.game import Game

def test_fps():
    game = Game(testRun=True)
    avgFps = game.run()

    assert avgFps > 60

def test_memory():
    game = Game(testRun=True)
    avgFps = game.run()

    process = psutil.Process()
    mem = process.memory_info().rss/1024  # in bytes 
    mem /= 1024

    assert mem < 62

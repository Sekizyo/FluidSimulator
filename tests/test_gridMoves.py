import modules.__config__ 
from modules.grid import Moves, Grid

class Test_getMoves():
    def setup_method(self):
        self.moves = Moves()
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_getMoves(self):
        value = self.moves.getMoves(0, 0, 1)
        assert value == [(0, 0), (0, 1), (1, 0)]

    def test_getMovesUnderBounds(self):
        value = self.moves.getMoves(-1, -1, 1)
        assert value == []

    def test_getMovesDepth2(self):
        value = self.moves.getMoves(0, 0, 2)
        assert value == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)]

class Test_getBlockValuesFromPosList():
    def setup_method(self):
        self.moves = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_getBlockValuesFromPosList(self):
        value = self.moves.getBlockValuesFromPosList([(0, 0)])
        assert value == [0]

    def test_getBlockValuesFromPosListNotWall(self):
        self.moves.blocks[0][0] = 1
        value = self.moves.getBlockValuesFromPosList([(0, 0)])
        assert value == [1]

    def test_getBlockValuesFromPosListMultiple(self):
        self.moves.blocks[0][0] = 1
        self.moves.blocks[0][1] = 0
        value = self.moves.getBlockValuesFromPosList([(0, 0), (0, 1)])
        assert value == [1, 0]

class Test_getAverageForList():
    def setup_method(self):
        self.moves = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_getAverageForList(self):
        assert self.moves.getAverageForList([1, 2, 3]) == 2

    def test_getAverageForListRounding(self):
        assert self.moves.getAverageForList([1, 2]) == 1.5

    def test_getAverageForListEmpty(self):
        assert self.moves.getAverageForList([]) == None

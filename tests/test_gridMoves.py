import modules.__config__ 
from modules.grid import Moves, Grid

class Test_getMoves():
    def setup_method(self):
        self.moves = Moves()
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_method(self):
        value = self.moves.getMoves(0, 0, 1)
        assert value == [(0, 0), (0, 1), (1, 0)]

    def test_Depth2(self):
        value = self.moves.getMoves(0, 0, 2)
        assert value == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)]

    def test_UnderBounds(self):
        value = self.moves.getMoves(-1, -1, 1)
        assert value == []

    def test_BeyondBounds(self):
        value = self.moves.getMoves(self.WIDTHBLOCKS+1, self.HEIGHTBLOCKS+1, 1)
        assert value == []

class Test_getBlockValuesFromPosList():
    def setup_method(self):
        self.moves = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_method(self):
        value = self.moves.getBlockValuesFromPosList([(0, 0)])
        assert value == [0]

    def test_NotWall(self):
        self.moves.blocks[0][0] = 1
        value = self.moves.getBlockValuesFromPosList([(0, 0)])
        assert value == [1]

    def test_MultipleInList(self):
        self.moves.blocks[0][0] = 1
        self.moves.blocks[0][1] = 0
        value = self.moves.getBlockValuesFromPosList([(0, 0), (0, 1)])
        assert value == [1, 0]

class Test_getAverageForList():
    def setup_method(self):
        self.moves = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_method(self):
        assert self.moves.getAverageForList([1, 2, 3]) == 2

    def test_Rounding(self):
        assert self.moves.getAverageForList([1, 2]) == 1.5

    def test_EmptyList(self):
        assert self.moves.getAverageForList([]) == None

import modules.__config__ 
from modules.grid import Position, Grid

class Test_checkBounds():
    def setup_method(self):
        self.position = Position()
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_method(self):
        assert self.position.checkBounds(self.WIDTHBLOCKS-1, self.HEIGHTBLOCKS-1) == True

    def test_ReturnValueTrue(self):
        assert type(self.position.checkBounds(1, 1)) == bool

    def test_UnderBounds(self):
        assert self.position.checkBounds(-1, -1) == False

    def test_UnderBoundsX(self):
        assert self.position.checkBounds(-1, self.HEIGHTBLOCKS-1) == False

    def test_UnderBoundsY(self):
        assert self.position.checkBounds(self.WIDTHBLOCKS-1, -1) == False

    def test_BeyondBounds(self):
        assert self.position.checkBounds(self.WIDTHBLOCKS+1, self.HEIGHTBLOCKS+1) == False

    def test_BeyondBoundsX(self):
        assert self.position.checkBounds(self.WIDTHBLOCKS+1, self.HEIGHTBLOCKS) == False

    def test_BeyondBoundsY(self):
        assert self.position.checkBounds(self.WIDTHBLOCKS, self.HEIGHTBLOCKS+1) == False


class Test_getGridPosFromPos():
    def setup_method(self):
        self.position = Position()

    def test_method(self):
        sizeX, sizeY = self.position.getGridPosFromPos((0,0))
        assert sizeX == 0
        assert sizeY == 0

class Test_getBlockValue():
    def setup_method(self):
        self.position = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_method(self):
        assert self.position.getBlockValue(0, 0) == 0 

    def test_UnderBounds(self):
        assert self.position.getBlockValue(-1, -1) == None 

    def test_UnderBoundsX(self):
        assert self.position.getBlockValue(-1, 0) == None 

    def test_UnderBoundsY(self):
        assert self.position.getBlockValue(0, -1) == None 

    def test_BeyondBounds(self):
        assert self.position.getBlockValue(self.WIDTHBLOCKS+1, self.HEIGHTBLOCKS+1) == None 

    def test_BeyondBoundsX(self):
        assert self.position.getBlockValue(self.WIDTHBLOCKS+1, 0) == None 

    def test_BeyondBoundsY(self):
        assert self.position.getBlockValue(0, self.HEIGHTBLOCKS+1) == None 

class Test_updateBlock():
    def setup_method(self):
        self.position = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_method(self):
        self.position.updateBlock(0, 0, 1)
        assert self.position.blocks[0][0] == 1

    def test_BlockWall(self):
        self.position.updateBlock(0, 0, -1)
        assert self.position.blocks[0][0] == -1

    def test_BlockWhereIsWall(self):
        self.position.blocks[0][0] = -1
        self.position.updateBlock(0, 0, 1)

        assert self.position.blocks[0][0] == -1

class Test_updateParticleCounter():
    def setup_method(self):
        self.position = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_method(self):
        self.position.updateParticleCounter(1)
        assert self.position.particleCounter == 1

    def test_Subtraction(self):
        self.position.updateParticleCounter(-1)
        assert self.position.particleCounter == -1
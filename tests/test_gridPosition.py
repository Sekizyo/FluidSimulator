import modules.__config__ 
from modules.grid import Position, Grid

class Test_checkBounds():
    def setup_method(self):
        self.position = Position()
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_checkBounds(self):
        assert self.position.checkBounds(self.WIDTHBLOCKS-1, self.HEIGHTBLOCKS-1) == True

    def test_checkBoundsOverScreen(self):
        assert self.position.checkBounds(self.WIDTHBLOCKS+1, self.HEIGHTBLOCKS+1) == False

    def test_checkBoundsOverScreenX(self):
        assert self.position.checkBounds(self.WIDTHBLOCKS+1, self.HEIGHTBLOCKS) == False

    def test_checkBoundsOverScreenY(self):
        assert self.position.checkBounds(self.WIDTHBLOCKS, self.HEIGHTBLOCKS+1) == False

    def test_checkBoundsUnderScreen(self):
        assert self.position.checkBounds(-1, -1) == False

    def test_checkBoundsUnderScreenX(self):
        assert self.position.checkBounds(-1, self.HEIGHTBLOCKS-1) == False

    def test_checkBoundsUnderScreenY(self):
        assert self.position.checkBounds(self.WIDTHBLOCKS-1, -1) == False

class Test_getGridPosFromPos():
    def setup_method(self):
        self.position = Position()

    def test_getGridPosFromPos(self):
        sizeX, sizeY = self.position.getGridPosFromPos((0,0))
        assert sizeX == 0
        assert sizeY == 0

class Test_getBlockValue():
    def setup_method(self):
        self.position = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_getBlockValue(self):
        assert self.position.getBlockValue(0, 0) == 0 

    def test_getBlockValueUnderBounds(self):
        assert self.position.getBlockValue(-1, -1) == None 

    def test_getBlockValueUnderBoundsX(self):
        assert self.position.getBlockValue(-1, 0) == None 

    def test_getBlockValueUnderBoundsY(self):
        assert self.position.getBlockValue(0, -1) == None 

    def test_getBlockValueOverBounds(self):
        assert self.position.getBlockValue(self.WIDTHBLOCKS+1, self.HEIGHTBLOCKS+1) == None 

    def test_getBlockValueOverBoundsX(self):
        assert self.position.getBlockValue(self.WIDTHBLOCKS+1, 0) == None 

    def test_getBlockValueOverBoundsY(self):
        assert self.position.getBlockValue(0, self.HEIGHTBLOCKS+1) == None 

class Test_updateBlock():
    def setup_method(self):
        self.position = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_updateBlock(self):
        self.position.updateBlock(0, 0, 1)
        assert self.position.blocks[0][0] == 1

    def test_updateBlockWall(self):
        self.position.updateBlock(0, 0, -1)
        assert self.position.blocks[0][0] == -1

    def test_updateBlockWhereIsWall(self):
        self.position.blocks[0][0] = -1
        self.position.updateBlock(0, 0, 1)

        assert self.position.blocks[0][0] == -1

class Test_updateParticleCounter():
    def setup_method(self):
        self.position = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_updateParticleCounter(self):
        self.position.updateParticleCounter(1)
        assert self.position.particleCounter == 1

    def test_updateParticleCounterSubtraction(self):
        self.position.updateParticleCounter(-1)
        assert self.position.particleCounter == -1
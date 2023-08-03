import modules.__config__ 
from modules.grid import Grid

class Test_createBlocks():
    def setup_method(self):
        self.controls = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_ReturnValue(self):
        assert self.controls.createBlocks() == None

    def test_BlocksLen(self):
        self.controls.createBlocks()
        assert len(self.controls.blocks) == self.WIDTHBLOCKS*2
        assert len(self.controls.blocks[0]) == self.HEIGHTBLOCKS

        assert len(self.controls.blockRect) == self.WIDTHBLOCKS*2
        assert len(self.controls.blockRect[0]) == self.HEIGHTBLOCKS

class Test_addParticle():
    def setup_method(self):
        self.controls = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS
        self.PARTICLESPERCLICK = modules.__config__.PARTICLESPERCLICK

    def test_method(self):
        self.controls.addParticle((0,0))
        assert self.controls.particleCounter == self.PARTICLESPERCLICK
        assert self.controls.blocks[0][0] == self.PARTICLESPERCLICK

    def test_ReturnValue(self):
        assert self.controls.createBlocks() == None
        
class Test_addWall():
    def setup_method(self):
        self.controls = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_method(self):
        self.controls.addWall((0, 0))
        assert self.controls.blocks[0][0] == -1
        
    def test_ReturnValue(self):
        assert self.controls.addWall((0, 0)) == None

    def test_UnderBounds(self):
        self.controls.addWall((-1, 0))
        assert self.controls.blocks[0][0] == 0
        
    def test_BeyondBounds(self):
        self.controls.addWall((self.WIDTHBLOCKS+1, self.HEIGHTBLOCKS+1))
        assert self.controls.blocks[0][0] == 0
        
class Test_reset():
    def setup_method(self):
        self.controls = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS
        self.HEIGHTBLOCKS = modules.__config__.HEIGHTBLOCKS

    def test_method(self):
        self.controls.reset()
        assert self.controls.particleCounter == 0
        
    def test_ReturnValue(self):
        assert self.controls.reset() == None

    def test_UnderBounds(self):
        self.controls.addWall((-1, 0))
        assert self.controls.blocks[0][0] == 0
        
    def test_BeyondBounds(self):
        self.controls.blocks[0][0] == 1
        self.controls.reset()
        assert self.controls.blocks[0][0] == 0

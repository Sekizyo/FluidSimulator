import modules.__config__ 
from modules.grid import Grid

class Test_update():
    def setup_method(self):
        self.diffusion = Grid(None)
        self.WIDTHBLOCKS = modules.__config__.WIDTHBLOCKS

    def test_method(self):
        self.diffusion.blocks[0][0] = 90
        self.diffusion.updateBlocks(0, 0)
        
        assert self.diffusion.blocks[0][0] == 30
        assert self.diffusion.blocks[1][0] == 30
        assert self.diffusion.blocks[0][1] == 30

    def test_ReturnValue(self):
        assert self.diffusion.update([[0]]) == None

    def test_BlocksReturnValue(self):
        assert self.diffusion.updateBlocks(0, 0) == None

    def test_UnderBounds(self):
        self.diffusion.blocks[-1][0] = 90
        self.diffusion.updateBlocks(0, 0)
        
        assert self.diffusion.blocks[0][0] == 0
        assert self.diffusion.blocks[1][0] == 0
        assert self.diffusion.blocks[0][1] == 0
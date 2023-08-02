
### Demo

![](https://github.com/Sekizyo/FluidSimulator/blob/bcc459f5174421ac359dfb098ebaa00560bfdec1/recources/demo1.mp4)   

![](https://github.com/Sekizyo/FluidSimulator/blob/bcc459f5174421ac359dfb098ebaa00560bfdec1/recources/demo2.mp4)   

### How to use

    py run.py
    
### Configuration

change in "__init__.py"

    WIDTH = 1000 - Screen width
    HEIGHT = 1000 - Screen height

    BLOCKSIZE = 10 - Scale block size, it greatly influences prerformance. Optimal values: 8 - 25

    DEPTH = 1 - Optimal values: 1-2 

    PARTICLESPERCLICK = 10000 - Optimal values: depends on BLOCKSIZE

### Controls

    Left mouse click - adds particles

    Right mouse click - adds walls

    R - resets screen

### Known issues

    When DEPTH is 2 or more, walls do not work
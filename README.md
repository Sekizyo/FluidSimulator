
### Demo



https://github.com/Sekizyo/FluidSimulator/assets/51287415/5b80bfac-e5a3-4c82-82d2-dcae9dd18863



https://github.com/Sekizyo/FluidSimulator/assets/51287415/9d48df9b-d8b5-4b4b-9fc8-d2fa283b5eb6


### How to use

    py run.py
    
### Configuration

change in "__config__.py"

    WIDTH = 1000 - Screen width
    HEIGHT = 1000 - Screen height

    BLOCKSIZE = 10 - Scale block size, it greatly influences prerformance. Optimal values: 8 - 25

    DEPTH = 1 - How far particle can spread. Optimal values: 1-2 
    VISCOSITY = 1 - its resistance to deformation at a given rate. Lower value more likely to spread. Optimal values: 1-100

    PARTICLESPERCLICK = 10000 - Optimal values: depends on BLOCKSIZE

### Controls

    Left mouse click - adds particles

    Right mouse click - adds walls

    R - resets screen

### Known issues

    When DEPTH is 2 or more, walls do not work

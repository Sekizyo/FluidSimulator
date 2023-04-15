import pygame
from random import randint, random, randrange
from modules import WIDTH, HEIGHT

class Particles():
    def __init__(self):
        self.particleCount = 0
        self.particles = pygame.sprite.Group()
        self.grid = []

    def create(self, amount, rectArea):
        self.particleCount += 1
        hue = randrange(360)
        radius, velocity = 5, 1
        pos_rect = rectArea.inflate(-radius * 2, -radius * 2)
        for i in range(amount):
            x = randrange(pos_rect.left, pos_rect.right)
            y = randrange(pos_rect.top, pos_rect.bottom)
            dir = pygame.math.Vector2(1, 0).rotate(randrange(360))
            particle = Particle(len(self.particles)+1, hue, (x, y), radius, dir, velocity)
            self.particles.add(particle)

    def draw(self, surface):
        self.particles.draw(surface)

    def update(self, rectArea):
        self.particles.update(rectArea)

    def colision(self):
        particle_list = self.particles.sprites()
        for i, particle_1 in enumerate(particle_list):
            for particle_2 in particle_list[i:]:
                distance_vec = particle_1.pos - particle_2.pos
                if 0 < distance_vec.length_squared() < (particle_1.radius + particle_2.radius) ** 2:
                    particle_1.dir.reflect_ip(distance_vec)
                    particle_2.dir.reflect_ip(distance_vec)
                    if abs(particle_1.hue - particle_2.hue) <= 180:
                        hue = (particle_1.hue + particle_2.hue) // 2
                    else:
                        hue = (particle_1.hue + particle_2.hue + 360) // 2 % 360
                    particle_1.changeColor(hue)
                    particle_2.changeColor(hue)
                    break

    def move(self):
        for particle in self.particles:
            particle.move()

    def render(self, rectArea):
        self.particles.update(rectArea)

class Particle(pygame.sprite.Sprite):
    def __init__(self,id, hue, pos, radius, dir, vel):
        super().__init__()
        self.id = id
        self.pos = pygame.math.Vector2(pos)
        self.dir = pygame.math.Vector2(dir)
        self.vel = vel
        self.radius = radius
        self.rect = pygame.Rect(round(self.pos.x - radius), round(self.pos.y - radius), radius*2, radius*2)
        self.image = pygame.Surface((radius*2, radius*2))
        self.changeColor(hue)

    def changeColor(self, hue):
        self.hue = hue
        color = pygame.Color(0)
        color.hsla = (self.hue, 100, 50, 100)
        self.image.set_colorkey((0, 0, 0))
        self.image.fill(0)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)

    def move(self):
        self.pos += self.dir * self.vel

    def update(self, border_rect):
        self.dir = self.dir/1.8 + pygame.math.Vector2(0, 0.5)

        if self.pos.x - self.radius < border_rect.left:
            self.pos.x = border_rect.left + self.radius
            self.dir.x = abs(self.dir.x)
        elif self.pos.x + self.radius > border_rect.right:
            self.pos.x = border_rect.right - self.radius
            self.dir.x = -abs(self.dir.x)
        if self.pos.y - self.radius < border_rect.top:
            self.pos.y = border_rect.top + self.radius
            self.dir.y = abs(self.dir.y)
        elif self.pos.y + self.radius > border_rect.bottom:
            self.pos.y = border_rect.bottom - self.radius
            self.dir.y = -abs(self.dir.y) 

        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))

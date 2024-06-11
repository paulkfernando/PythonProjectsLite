#This is my first little mini project outside of school that I've done in python.
#Most of the content taught in lectures revolved around algorithms, and without repetitive use of python,
#I felt that my knowledge and ability to use the language needs some suplmentation, so I will try my 
#hand at a few simple projects.

#This code, simulates particles, for now there isn't much real physics being implemented here except for
#the idea of collisions, but I will try and add new features to this on an ongoing basis.

import pygame
import random
import math

#function to calculate elastic collisions

def calcVel (v1, theta1, m1, v2, theta2, m2):
    rad1 = math.radians(theta1)
    rad2 = math.radians(theta2)

    p1_initial = m1*v1
    p2_initial = m2*v2

    p1_ix = p1_initial * math.cos(rad1)
    p1_iy = p1_initial * math.sin(rad1)
    p2_ix = p2_initial * math.cos(rad2)
    p2_iy = p2_initial * math.sin(rad2)    

    totpix = p1_ix + p2_ix
    totpiy = p2_iy + p1_iy

    totm = m1+m2

    return totpix/totm, totpiy/totpiy

#class created for Particles
class Particle:
    #initialization
    def __init__(self, screen, x, y, radius, color):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        #[-1, 1] determines direction, (1, 5) defines speed
        self.dx = random.choice([-1, 1])*random.randint(1, 5)
        self.dy = random.choice([-1, 1])*random.randint(1, 5)
    
    #move the particle
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
        if self.x - self.radius < 0 or self.x + self.radius > self.screen.get_width():
            self.dx *= -1
        if self.y - self.radius < 0 or self.y + self.radius > self.screen.get_height():
            self.dy *= -1

    #detect for particle collision
    def collision(self, other):
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y)**2)
        return distance < self.radius
    
    #handle collicion
    def handle_collision(self, other):
        theta_slf = math.atan2(self.dy, self.dx)
        theta_oth = math.atan2(other.dy, other.dx)
        slf_vel = math.sqrt((self.dx ** 2) + (self.dy ** 2))
        oth_vel = math.sqrt((other.dx ** 2) + (other.dy ** 2))

        vfx, vfy = calcVel(slf_vel, theta_slf, 1, oth_vel, theta_oth, 3)

        self.dx = vfx
        self.dy = vfy

        other.dx = -vfx
        other.dy = -vfy





    #draw the particle
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)


def main():
    pygame.init()
    
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    #initialize a list of particles
    particles = [Particle(screen, random.randint(3, 497), random.randint(3, 497), 10, (0, 0, 255)) for _ in range(10)]

    collision_counter = 0
    running = True



    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        for i, particle in enumerate(particles):
            for j in range(i + 1, len(particles)):
                if particle.collision(particles[j]):
                    particle.handle_collision(particles[j])
                    collision_counter += 1

        for particle in particles:
            particle.move()
            particle.draw()

        font = pygame.font.Font(None, 36)
        txt = font.render(f"Collision: {collision_counter}", True, (0,0,0))
        screen.blit(txt, (10, 10))

        pygame.display.flip() #Update display contents

        clock.tick(60) #60 Frames a second

    pygame.quit()

if __name__ == "__main__":
    main()
import pygame, math
from pygame.math import Vector2
import random
from math import fabs, atan, pi

SCREEN_WIDTH = 1277
SCREEN_HEIGHT = 666
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

class Boid:

    def __init__(self, x, y):
        self.positionX = x
        self.positionY = y
        self.velocityX = random.uniform(-10,10)
        self.velocityY = random.uniform(-10,10)


    def distance(self, neighbour):
        """Calculate the distance to another boid"""

        Rx = self.positionX - neighbour.positionX
        if Rx>float(SCREEN_WIDTH)/2.0:
            Rx=SCREEN_WIDTH-Rx
        Ry = self.positionY - neighbour.positionY
        if Ry>float(SCREEN_HEIGHT)/2.0:
            Ry=SCREEN_HEIGHT-Ry

        return math.sqrt(Rx**2 + Ry**2)

    def alignment(self, flock, weight):
        """ Move with the flock """

        if len(flock) < 1:
            return

        Vx = 0
        Vy = 0

        for boid in flock:
            Vx += boid.velocityX
            Vy += boid.velocityY

        Vx /= len(flock)
        Vy /= len(flock)

        self.velocityX += weight * (Vx - self.velocityX)
        self.velocityY += weight * (Vy - self.velocityY)

    def separation(self, flock, min_distance, weight):
        """ Avoid crowding """

        if len(flock) < 1:
            return

        for boid in flock:
            distance = self.distance(boid)

            if distance < min_distance:
                xdiff = (-self.positionX + boid.positionX)
                if math.fabs(xdiff)>float(SCREEN_WIDTH)/2.0:
                    xdiff=-math.copysign(100-abs(xdiff),xdiff)
                ydiff = (-self.positionY + boid.positionY)
                if math.fabs(ydiff)>float(SCREEN_HEIGHT)/2.0:
                    ydiff=-math.copysign(100-abs(ydiff),ydiff)

                self.velocityX -= xdiff * weight
                self.velocityY -= ydiff * weight

    def cohesion(self, flock, weight):
        """ Move closer to the flock """

        if len(flock) < 1:
            return

        Rx = 0
        Ry = 0
        for boid in flock:
            xdiff = (-self.positionX + boid.positionX)
            if math.fabs(xdiff)>float(SCREEN_WIDTH)/2.0:
                Rx+=boid.positionX-math.copysign(SCREEN_WIDTH,xdiff)
            else:
                Rx+=boid.positionX
            ydiff = (-self.positionY + boid.positionY)
            if math.fabs(ydiff)>float(SCREEN_HEIGHT)/2.0:
                Ry+=boid.positionY-math.copysign(SCREEN_HEIGHT,ydiff)
            else:
                Ry+=boid.positionY

        Rx /= len(flock)
        Ry /= len(flock)

        self.velocityX += weight * (Rx - self.positionX)
        self.velocityY += weight * (Ry - self.positionY)

    def update(self, max_velocity):

        # boundry conditions
        if self.positionX < 0 and self.velocityX < 0:
            self.positionX = SCREEN_WIDTH
        if self.positionX > SCREEN_WIDTH and self.velocityX > 0:
            self.positionX = 0
        if self.positionY < 0 and self.velocityY < 0:
            self.positionY = SCREEN_HEIGHT
        if self.positionY > SCREEN_HEIGHT and self.velocityY > 0:
            self.positionY = 0

        # maximum speed
        sp=math.sqrt(self.velocityX**2+self.velocityY**2)
        if sp>max_velocity:
            self.velocityX*=max_velocity/sp
            self.velocityY*=max_velocity/sp

        self.positionX += self.velocityX
        self.positionY += self.velocityY

    def is_neighbour(self, neighbour, D, alpha):
        dist = self.distance(neighbour)
        xx=neighbour.positionX
        xdiff=neighbour.positionX - self.positionX
        if math.fabs(xdiff)>float(SCREEN_WIDTH)/2.0:
            xx=xx-math.copysign(SCREEN_WIDTH,xdiff)
        yy=neighbour.positionY
        ydiff=neighbour.positionY - self.positionY
        if math.fabs(ydiff)>float(SCREEN_HEIGHT)/2.0:
            yy=yy-math.copysign(SCREEN_HEIGHT,ydiff)
        angle = fabs(atan(self.velocityY / (self.velocityX + 0.00001)) - atan(
            (yy - self.positionY) / (xx - self.positionX + 0.00001)))
        if (dist <= D and angle <= alpha):
            return True
        else:
            return False

    def goal(self, mouse_x, mouse_y, weight, on):
        """Seek goal"""
        if on:
            self.velocityX += (mouse_x - self.positionX) * weight
            self.velocityY += (mouse_y - self.positionY) * weight
        else:
            self.positionX += self.velocityX
            self.positionY += self.velocityY

    def avoid(self, obstacle, weight):
        """Avoid obstacles"""

        self.velocityX -= (obstacle.positionX - self.positionX) * weight
        self.velocityY -= (obstacle.positionY - self.positionY) * weight

    def draw(self):

        velocity = Vector2(self.velocityX, self.velocityY)
        position = Vector2(self.positionX, self.positionY)
        phi = velocity.angle_to(Vector2(0,1))

        points = [Vector2(0,20), Vector2(4,4), Vector2(-4,4)]
        points = [p.rotate(phi) for p in points]
        points = [Vector2(p.x*-1,p.y) for p in points]
        points = [position+p*2 for p in points]
        pygame.draw.polygon(screen, [0,0,0], points)


class Obstacle:

    def __init__(self, x, y):
        self.positionX = x
        self.positionY = y

    def draw(self):
        pygame.draw.circle(screen, (102, 102, 253), [self.positionX, self.positionY], 30, 0)
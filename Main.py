import pygame, math
from Boid import *

# PARAMETERS
weight_alignement = 1.0
weight_cohesion = 0.01
weight_separation = 0.2
weight_avoid = 0.2
weight_goal = 0.1
delta_time = 0.0
max_fps = 40

# Start simulation
pygame.init()
clock = pygame.time.Clock()
running = True

flock = []
obstacles = []

background_image = pygame.image.load("sky.png").convert()
while running:

    goal_on = False
    mouse_x = 0
    mouse_y = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      # add boid with left mouse click
            pos = pygame.mouse.get_pos()
            boid = Boid(pos[0],pos[1])
            flock.append(boid)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:      # give boids goal with middle mouse click
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            goal_on = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:      # add obstacles with right mouse click
            pos = pygame.mouse.get_pos()
            obstacle = Obstacle(pos[0],pos[1])
            obstacles.append(obstacle)


    delta_time += clock.tick() / 1000.0
    if (delta_time > (1 / max_fps)):
        delta_time = delta_time - (1 / max_fps)

        screen.fill((0, 0, 0))
        screen.blit(background_image,[0,0])
        for boid in flock:
            neighbourhood = []
            for neighbour in flock:
                if neighbour == boid:
                    continue
                d = boid.distance(neighbour)
                if boid.is_neighbour(neighbour, 100.0, (120.0 * pi) / 180.0):
                    neighbourhood.append(neighbour)

            # follow rules
            boid.alignment(neighbourhood, weight_alignement)
            boid.cohesion(neighbourhood, weight_cohesion)
            boid.separation(neighbourhood, 60.0, weight_cohesion)
            for obstacle in obstacles:
                d = boid.distance(obstacle)
                if d < 80:
                    boid.avoid(obstacle, weight_avoid)
                obstacle.draw()
            boid.goal(mouse_x, mouse_y, weight_goal, goal_on)
            boid.update(5)
            boid.draw()

    pygame.display.update()
pygame.quit()
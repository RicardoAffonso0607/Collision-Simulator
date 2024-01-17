
# Ricardo Rodrigues Affonso 

from random import randint
import pygame

# Set the window parameters
Width, Height = 1440, 766
Display = pygame.display.set_mode((Width, Height))

# Define the background_color
background_color = (0, 0, 0)

# Define the FPS
FPS = 60

# Create a list for the balls
balls_list = []

# The number of balls can be changed
balls_number = 50 

# Define the balls size
diameter = 36
radius = diameter/2

# Define mass and velocity
m = radius**2
v = 7


def main():
    clock = pygame.time.Clock()
    run = True

    # Create the balls
    for i in range(balls_number):
        balls_list.append(balls(randint(radius, Width - radius), randint(radius, Height - radius), randint(-v, v), randint(-v, v), color()))

        # Don't let the balls spawn above others
        colidiu = True
        while colidiu:
            colidiu = False
            for j in range(0, i):
                if dist_centers(balls_list[i].x, balls_list[i].y, balls_list[j].x, balls_list[j].y) < diameter**2:
                    balls_list.pop(i)
                    balls_list.append(balls(randint(radius, Width - radius), randint(radius, Height - radius), randint(0, v), randint(0, v), color()))
                    colidiu = True
                    break
    
    # Execute the moving
    while run:
        clock.tick(FPS)

        # Close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Execute all the interactions with the balls
        for i in range(balls_number):
            balls_list[i].collision(i)
            balls_list[i].change_position()
            balls_list[i].wall_collision()

        print(kinects_energy_total())

        # Update the window
        draw_window()

    pygame.quit()


class balls:

    def __init__ (self, x, y, vx, vy, color):
        self.x = x # position (x)
        self.y = y # position (y)
        self.vx = vx # velocity (x)
        self.vy = vy # velocity (y)
        self.color = color 
        self.col_ant = -5 # to happen only one collision

    # Change the position
    def change_position (self):
        self.y = self.vy + self.y
        self.x = self.vx + self.x

    # Change the direction of the component who collided
    def wall_collision (self):
        if self.y + radius > Height and self.vy > 0:
            self.vy = -self.vy
            self.col_ant = -1

        if self.y < radius and self.vy < 0:
            self.vy = -self.vy
            self.col_ant = -1

        if self.x + radius > Width and self.vx > 0:
            self.vx = -self.vx
            self.col_ant = -1

        if self.x < radius and self.vx < 0:
            self.vx = - self.vx
            self.col_ant = -1

    # Draw the balls in the window
    def draw_ball(self, i):
        pygame.draw.circle(Display, self.color, (self.x, self.y), radius)

    # Do the collision between the balls
    def collision(self, i):
        for j in range(i+1, balls_number):

            if dist_centers(self.x, self.y, balls_list[j].x, balls_list[j].y) < diameter**2:
                if self.col_ant != j or balls_list[j].ultcol != i:

                    # Do the projection in the direction of the collision
                    proj1, proj2 = ortogonal_projection(self.vx, self.vy, self.x - balls_list[j].x, self.y - balls_list[j].y)
                    proj3, proj4 = ortogonal_projection(balls_list[j].vx, balls_list[j].vy, self.x - balls_list[j].x, self.y - balls_list[j].y)

                    # Change the direction of the velocity
                    self.vx = self.vx -proj1 +proj3
                    self.vy = self.vy -proj2 +proj4
                    balls_list[j].vx = balls_list[j].vx +proj1 -proj3
                    balls_list[j].vy = balls_list[j].vy +proj2 -proj4
                    self.col_ant = j
                    balls_list[j].ultcol = i

# Generates a random color
def color ():
    colorido = randint(70, 200), randint (70, 200), randint (70, 200)
    return colorido

# Do the projection of the velocity
def ortogonal_projection (v1, v2, u1, u2):
    prop = (((u1*v1) + (u2*v2)) / ((u1*u1) + (u2*u2)))
    return u1*prop, u2*prop

# Calculates the dist between two centers
def dist_centers(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2

# Create and draw the window
def draw_window():
    Display.fill((background_color))
    for i in range(balls_number):
        balls_list[i].draw_ball(i)
    pygame.display.update()

# Calculates the total kinects energy
def kinects_energy_total():
    energia = 0
    for i in range(balls_number):
        energia += ((balls_list[i].vx**2) + (balls_list[i].vy**2)) * m / 2
    return energia

if __name__ == "__main__":
    main()
import pygame
import topography
import simpleGeometry

pygame.init()
size = [600, 600]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Topography Map")
done = False
clock = pygame.time.Clock()

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

cp = simpleGeometry.simplePoint(300,300)
mountain = topography.contour_group(cp, 15, 1, False)
mountain.define_start(5, 15, 8)
mountain.define_displacements(5, 300)
mountain.generate()

while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
	clock.tick(1)
     
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop
 
    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.
     
    # Clear the screen and set the screen background
	screen.fill(WHITE)
    # This draws a triangle using the polygon command
    #pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 0)
	
	mountain.draw(screen)
    
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
	pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()